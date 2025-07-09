#!/usr/bin/env python3
"""
数据库管理模块
用于存储活动记录和总结
"""

import sqlite3
import os
import logging
from datetime import datetime, date
from typing import List, Dict, Optional

class DatabaseManager:
    def __init__(self, config):
        self.config = config
        self.db_path = config['storage']['database']
        self.data_dir = config['storage']['data_dir']
        
        # 确保数据目录存在
        os.makedirs(self.data_dir, exist_ok=True)
        
        # 设置日志
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # 初始化数据库
        self._init_database()
    
    def _init_database(self):
        """初始化数据库表"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # 创建活动记录表
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS activities (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp DATETIME NOT NULL,
                        date DATE NOT NULL,
                        description TEXT NOT NULL,
                        screenshot_path TEXT,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # 创建每日总结表
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS daily_summaries (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date DATE UNIQUE NOT NULL,
                        summary TEXT NOT NULL,
                        activity_count INTEGER NOT NULL,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # 创建索引
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_activities_date ON activities(date)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_activities_timestamp ON activities(timestamp)')
                
                conn.commit()
                self.logger.info("数据库初始化成功")
                
        except Exception as e:
            self.logger.error(f"数据库初始化失败: {str(e)}")
    
    def add_activity(self, description: str, screenshot_path: Optional[str] = None) -> bool:
        """
        添加活动记录
        参数:
            description: 活动描述
            screenshot_path: 截图路径（可选）
        返回: 是否成功
        """
        try:
            current_time = datetime.now()
            current_date = current_time.date()
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO activities (timestamp, date, description, screenshot_path)
                    VALUES (?, ?, ?, ?)
                ''', (current_time, current_date, description, screenshot_path))
                
                conn.commit()
                self.logger.info(f"活动记录已添加: {description[:50]}...")
                return True
                
        except Exception as e:
            self.logger.error(f"添加活动记录失败: {str(e)}")
            return False
    
    def get_activities_by_date(self, target_date: date) -> List[Dict]:
        """
        获取指定日期的活动记录
        参数: target_date - 目标日期
        返回: 活动记录列表
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT timestamp, description, screenshot_path
                    FROM activities
                    WHERE date = ?
                    ORDER BY timestamp
                ''', (target_date,))
                
                activities = []
                for row in cursor.fetchall():
                    activities.append({
                        'timestamp': row[0],
                        'description': row[1],
                        'screenshot_path': row[2]
                    })
                
                return activities
                
        except Exception as e:
            self.logger.error(f"获取活动记录失败: {str(e)}")
            return []
    
    def get_today_activities(self) -> List[Dict]:
        """获取今天的活动记录"""
        return self.get_activities_by_date(date.today())
    
    def save_daily_summary(self, target_date: date, summary: str) -> bool:
        """
        保存每日总结
        参数:
            target_date: 目标日期
            summary: 总结内容
        返回: 是否成功
        """
        try:
            # 获取当日活动数量
            activities = self.get_activities_by_date(target_date)
            activity_count = len(activities)
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # 使用REPLACE来更新或插入
                cursor.execute('''
                    REPLACE INTO daily_summaries (date, summary, activity_count)
                    VALUES (?, ?, ?)
                ''', (target_date, summary, activity_count))
                
                conn.commit()
                self.logger.info(f"每日总结已保存: {target_date}")
                return True
                
        except Exception as e:
            self.logger.error(f"保存每日总结失败: {str(e)}")
            return False
    
    def get_daily_summary(self, target_date: date) -> Optional[Dict]:
        """
        获取指定日期的总结
        参数: target_date - 目标日期
        返回: 总结信息字典或None
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT summary, activity_count, created_at
                    FROM daily_summaries
                    WHERE date = ?
                ''', (target_date,))
                
                row = cursor.fetchone()
                if row:
                    return {
                        'date': target_date,
                        'summary': row[0],
                        'activity_count': row[1],
                        'created_at': row[2]
                    }
                return None
                
        except Exception as e:
            self.logger.error(f"获取每日总结失败: {str(e)}")
            return None
    
    def get_activity_stats(self, days: int = 7) -> Dict:
        """
        获取活动统计信息
        参数: days - 统计天数（默认7天）
        返回: 统计信息字典
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # 总活动数
                cursor.execute('''
                    SELECT COUNT(*) FROM activities
                    WHERE date >= date('now', '-{} days')
                '''.format(days))
                total_activities = cursor.fetchone()[0]
                
                # 每日平均活动数
                cursor.execute('''
                    SELECT COUNT(DISTINCT date) FROM activities
                    WHERE date >= date('now', '-{} days')
                '''.format(days))
                active_days = cursor.fetchone()[0]
                
                avg_activities = total_activities / max(active_days, 1)
                
                # 最活跃的日期
                cursor.execute('''
                    SELECT date, COUNT(*) as activity_count
                    FROM activities
                    WHERE date >= date('now', '-{} days')
                    GROUP BY date
                    ORDER BY activity_count DESC
                    LIMIT 1
                '''.format(days))
                
                most_active_day = cursor.fetchone()
                
                return {
                    'period_days': days,
                    'total_activities': total_activities,
                    'active_days': active_days,
                    'avg_activities_per_day': round(avg_activities, 2),
                    'most_active_day': most_active_day[0] if most_active_day else None,
                    'most_active_day_count': most_active_day[1] if most_active_day else 0
                }
                
        except Exception as e:
            self.logger.error(f"获取活动统计失败: {str(e)}")
            return {}
    
    def cleanup_old_data(self, days_to_keep: int = 30):
        """
        清理旧数据
        参数: days_to_keep - 保留天数（默认30天）
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # 删除旧的活动记录
                cursor.execute('''
                    DELETE FROM activities
                    WHERE date < date('now', '-{} days')
                '''.format(days_to_keep))
                
                deleted_activities = cursor.rowcount
                
                # 删除旧的总结
                cursor.execute('''
                    DELETE FROM daily_summaries
                    WHERE date < date('now', '-{} days')
                '''.format(days_to_keep))
                
                deleted_summaries = cursor.rowcount
                
                conn.commit()
                self.logger.info(f"数据清理完成: 删除了 {deleted_activities} 条活动记录, {deleted_summaries} 条总结")
                
        except Exception as e:
            self.logger.error(f"数据清理失败: {str(e)}")