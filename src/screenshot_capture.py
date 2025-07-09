#!/usr/bin/env python3
"""
屏幕截图捕获模块
支持macOS系统的屏幕截图功能
"""

import os
import subprocess
import time
from datetime import datetime
from PIL import Image
import logging

class ScreenshotCapture:
    def __init__(self, config):
        self.config = config
        self.screenshots_dir = config['storage']['screenshots_dir']
        self.save_screenshots = config['screenshot']['save_screenshots']
        self.quality = config['screenshot']['screenshot_quality']
        
        # 确保截图目录存在
        os.makedirs(self.screenshots_dir, exist_ok=True)
        
        # 设置日志
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def capture_screenshot(self):
        """
        捕获屏幕截图
        返回: (screenshot_path, success)
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            temp_path = f"/tmp/screenshot_{timestamp}.png"
            
            # 使用macOS的screencapture命令
            result = subprocess.run([
                'screencapture', 
                '-x',  # 不播放声音
                '-T', '1',  # 1秒延迟
                temp_path
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                self.logger.error(f"截图失败: {result.stderr}")
                return None, False
            
            # 如果需要保存截图
            if self.save_screenshots:
                final_path = os.path.join(self.screenshots_dir, f"screenshot_{timestamp}.jpg")
                
                # 使用PIL转换为JPEG并压缩
                with Image.open(temp_path) as img:
                    # 转换为RGB模式（去除alpha通道）
                    if img.mode in ('RGBA', 'LA'):
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                        img = background
                    
                    img.save(final_path, 'JPEG', quality=self.quality, optimize=True)
                
                # 删除临时文件
                os.remove(temp_path)
                self.logger.info(f"截图已保存: {final_path}")
                return final_path, True
            else:
                self.logger.info("截图捕获成功（未保存到磁盘）")
                return temp_path, True
                
        except Exception as e:
            self.logger.error(f"截图过程出错: {str(e)}")
            return None, False
    
    def get_screenshot_for_analysis(self):
        """
        获取用于AI分析的截图
        返回: PIL Image对象
        """
        try:
            temp_path = "/tmp/temp_screenshot_for_analysis.png"
            
            result = subprocess.run([
                'screencapture', 
                '-x',
                '-T', '1',
                temp_path
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                self.logger.error(f"分析截图失败: {result.stderr}")
                return None
            
            # 打开图片
            img = Image.open(temp_path)
            
            # 转换为RGB模式
            if img.mode in ('RGBA', 'LA'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            
            # 删除临时文件
            os.remove(temp_path)
            
            return img
            
        except Exception as e:
            self.logger.error(f"获取分析截图出错: {str(e)}")
            return None