#!/usr/bin/env python3
"""
AI识别总结工具主程序
基于本地Ollama的离线屏幕活动分析和总结工具
"""

import os
import sys
import time
import yaml
import schedule
import logging
import signal
from datetime import datetime, date, time as dt_time
from threading import Thread, Event

# 添加src目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from screenshot_capture import ScreenshotCapture
from ollama_client import OllamaClient
from database_manager import DatabaseManager

class ActivityTracker:
    def __init__(self, config_path='config.yaml'):
        """初始化活动追踪器"""
        # 加载配置
        self.config = self._load_config(config_path)
        
        # 设置日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('activity_tracker.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # 初始化组件
        self.screenshot_capture = ScreenshotCapture(self.config)
        self.ollama_client = OllamaClient(self.config)
        self.db_manager = DatabaseManager(self.config)
        
        # 运行状态
        self.running = False
        self.stop_event = Event()
        
        # 记录上一次分析结果，避免重复记录相同活动
        self.last_analysis = ""
        self.last_analysis_time = None
        
        self.logger.info("活动追踪器初始化完成")
    
    def _load_config(self, config_path):
        """加载配置文件"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            return config
        except Exception as e:
            print(f"加载配置文件失败: {e}")
            sys.exit(1)
    
    def analyze_current_activity(self):
        """分析当前活动"""
        try:
            # 捕获截图
            image = self.screenshot_capture.get_screenshot_for_analysis()
            if not image:
                self.logger.warning("截图捕获失败，跳过本次分析")
                return
            
            # AI分析
            analysis = self.ollama_client.analyze_screenshot(image)
            if not analysis:
                self.logger.warning("AI分析失败，跳过本次记录")
                return
            
            # 检查是否与上次分析结果相似，避免重复记录
            if self._is_similar_activity(analysis):
                self.logger.debug("活动与上次相似，跳过记录")
                return
            
            # 保存截图（如果配置要求）
            screenshot_path = None
            if self.config['screenshot']['save_screenshots']:
                screenshot_path, success = self.screenshot_capture.capture_screenshot()
                if not success:
                    screenshot_path = None
            
            # 存储到数据库
            success = self.db_manager.add_activity(analysis, screenshot_path)
            if success:
                self.logger.info(f"新活动记录: {analysis[:100]}...")
                self.last_analysis = analysis
                self.last_analysis_time = datetime.now()
            
        except Exception as e:
            self.logger.error(f"分析活动时出错: {str(e)}")
    
    def _is_similar_activity(self, current_analysis):
        """判断当前分析结果是否与上次相似"""
        if not self.last_analysis or not self.last_analysis_time:
            return False
        
        # 如果距离上次分析不到5分钟且内容相似度高，则认为是相同活动
        time_diff = (datetime.now() - self.last_analysis_time).total_seconds()
        if time_diff < 300:  # 5分钟
            # 简单的相似度检查（可以改进为更复杂的算法）
            similarity = self._calculate_similarity(current_analysis, self.last_analysis)
            return similarity > 0.8
        
        return False
    
    def _calculate_similarity(self, text1, text2):
        """计算两个文本的相似度（简单实现）"""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 and not words2:
            return 1.0
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union)
    
    def generate_daily_summary(self):
        """生成每日总结"""
        try:
            today = date.today()
            activities = self.db_manager.get_activities_by_date(today)
            
            if not activities:
                self.logger.info("今天没有活动记录，跳过总结生成")
                return
            
            self.logger.info(f"开始生成 {today} 的每日总结，共 {len(activities)} 条活动记录")
            
            # 使用AI生成总结
            summary = self.ollama_client.generate_daily_summary(activities)
            if summary:
                # 保存总结
                success = self.db_manager.save_daily_summary(today, summary)
                if success:
                    self.logger.info("每日总结生成并保存成功")
                    print(f"\n{'='*50}")
                    print(f"📊 {today} 每日总结")
                    print(f"{'='*50}")
                    print(summary)
                    print(f"{'='*50}\n")
                else:
                    self.logger.error("每日总结保存失败")
            else:
                self.logger.error("每日总结生成失败")
                
        except Exception as e:
            self.logger.error(f"生成每日总结时出错: {str(e)}")
    
    def setup_schedule(self):
        """设置定时任务"""
        # 设置截图和分析的定时任务
        interval = self.config['screenshot']['interval_minutes']
        schedule.every(interval).minutes.do(self.analyze_current_activity)
        
        # 设置每日总结任务
        summary_time = self.config['summary']['daily_summary_time']
        schedule.every().day.at(summary_time).do(self.generate_daily_summary)
        
        # 设置数据清理任务（每周执行一次）
        schedule.every().week.do(self.db_manager.cleanup_old_data)
        
        self.logger.info(f"定时任务已设置: 每{interval}分钟分析一次，每天{summary_time}生成总结")
    
    def check_dependencies(self):
        """检查依赖是否满足"""
        self.logger.info("检查系统依赖...")
        
        # 检查Ollama连接
        if not self.ollama_client.test_connection():
            self.logger.error("无法连接到Ollama服务")
            print("\n❌ Ollama连接失败！")
            print("请确保:")
            print("1. Ollama已安装并运行")
            print("2. 已下载llava模型: ollama pull llava")
            print("3. Ollama服务运行在 http://localhost:11434")
            return False
        
        # 检查截图权限（macOS）
        try:
            test_image = self.screenshot_capture.get_screenshot_for_analysis()
            if test_image is None:
                self.logger.error("截图功能测试失败")
                print("\n❌ 截图权限不足！")
                print("请在 系统偏好设置 > 安全性与隐私 > 隐私 > 屏幕录制 中添加终端权限")
                return False
        except Exception as e:
            self.logger.error(f"截图测试失败: {str(e)}")
            return False
        
        self.logger.info("✅ 所有依赖检查通过")
        return True
    
    def start(self):
        """启动活动追踪器"""
        if not self.check_dependencies():
            return False
        
        # 设置定时任务
        self.setup_schedule()
        
        # 设置信号处理
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        self.running = True
        
        print("\n🚀 AI活动追踪器已启动")
        print(f"📸 每{self.config['screenshot']['interval_minutes']}分钟自动截图分析")
        print(f"📊 每天{self.config['summary']['daily_summary_time']}生成总结")
        print("按 Ctrl+C 停止运行\n")
        
        # 立即执行一次分析
        self.analyze_current_activity()
        
        # 主循环
        try:
            while self.running and not self.stop_event.is_set():
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        
        self.logger.info("活动追踪器已停止")
        return True
    
    def _signal_handler(self, signum, frame):
        """信号处理器"""
        self.logger.info(f"接收到信号 {signum}，准备停止...")
        self.running = False
        self.stop_event.set()
    
    def show_stats(self):
        """显示统计信息"""
        print("\n📈 活动统计")
        print("="*40)
        
        stats = self.db_manager.get_activity_stats()
        if stats:
            print(f"📅 统计周期: 最近{stats['period_days']}天")
            print(f"📊 总活动次数: {stats['total_activities']}")
            print(f"🗓️ 活跃天数: {stats['active_days']}")
            print(f"📈 日均活动: {stats['avg_activities_per_day']}")
            if stats['most_active_day']:
                print(f"🔥 最活跃日期: {stats['most_active_day']} ({stats['most_active_day_count']}次)")
        
        # 显示今日总结
        today = date.today()
        summary = self.db_manager.get_daily_summary(today)
        if summary:
            print(f"\n📋 今日总结 ({today})")
            print("="*40)
            print(summary['summary'])
        
        print()

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='AI活动识别总结工具')
    parser.add_argument('--config', default='config.yaml', help='配置文件路径')
    parser.add_argument('--stats', action='store_true', help='显示统计信息')
    parser.add_argument('--summary', action='store_true', help='生成今日总结')
    
    args = parser.parse_args()
    
    # 创建活动追踪器
    tracker = ActivityTracker(args.config)
    
    if args.stats:
        tracker.show_stats()
        return
    
    if args.summary:
        tracker.generate_daily_summary()
        return
    
    # 启动主程序
    tracker.start()

if __name__ == "__main__":
    main()