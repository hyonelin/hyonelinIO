#!/usr/bin/env python3
"""
Ollama客户端模块
用于与本地Ollama服务交互，进行图像分析
"""

import requests
import json
import base64
import io
import logging
from PIL import Image

class OllamaClient:
    def __init__(self, config):
        self.config = config
        self.base_url = config['ollama']['base_url']
        self.model = config['ollama']['model']
        self.timeout = config['ollama']['timeout']
        self.system_prompt = config['analysis']['system_prompt']
        
        # 设置日志
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def _image_to_base64(self, image):
        """
        将PIL Image转换为base64字符串
        """
        try:
            buffer = io.BytesIO()
            # 确保图像是RGB模式
            if image.mode != 'RGB':
                image = image.convert('RGB')
            image.save(buffer, format='JPEG', quality=85)
            buffer.seek(0)
            return base64.b64encode(buffer.read()).decode('utf-8')
        except Exception as e:
            self.logger.error(f"图像转换base64失败: {str(e)}")
            return None
    
    def analyze_screenshot(self, image):
        """
        分析屏幕截图
        参数: image - PIL Image对象
        返回: 分析结果字符串
        """
        try:
            # 转换图像为base64
            image_base64 = self._image_to_base64(image)
            if not image_base64:
                return None
            
            # 准备请求数据
            payload = {
                "model": self.model,
                "prompt": self.system_prompt,
                "images": [image_base64],
                "stream": False
            }
            
            # 发送请求到Ollama
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                analysis = result.get('response', '').strip()
                self.logger.info("图像分析成功")
                return analysis
            else:
                self.logger.error(f"Ollama请求失败: {response.status_code}, {response.text}")
                return None
                
        except requests.exceptions.ConnectionError:
            self.logger.error("无法连接到Ollama服务，请确保Ollama正在运行")
            return None
        except requests.exceptions.Timeout:
            self.logger.error("Ollama请求超时")
            return None
        except Exception as e:
            self.logger.error(f"分析截图时出错: {str(e)}")
            return None
    
    def generate_daily_summary(self, activities):
        """
        生成每日总结
        参数: activities - 当日活动列表
        返回: 总结字符串
        """
        try:
            # 构建活动记录文本
            activities_text = "\n".join([
                f"{activity['timestamp']}: {activity['description']}"
                for activity in activities
            ])
            
            # 准备总结提示
            summary_prompt = f"""
            {self.config.get('summary', {}).get('summary_prompt', '')}
            
            以下是今天的活动记录：
            {activities_text}
            """
            
            payload = {
                "model": self.model.replace('llava', 'llama2'),  # 使用文本模型进行总结
                "prompt": summary_prompt,
                "stream": False
            }
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=self.timeout * 2  # 总结可能需要更长时间
            )
            
            if response.status_code == 200:
                result = response.json()
                summary = result.get('response', '').strip()
                self.logger.info("每日总结生成成功")
                return summary
            else:
                self.logger.error(f"总结生成失败: {response.status_code}, {response.text}")
                return None
                
        except Exception as e:
            self.logger.error(f"生成每日总结时出错: {str(e)}")
            return None
    
    def test_connection(self):
        """
        测试与Ollama的连接
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                self.logger.info(f"成功连接到Ollama，可用模型: {[m['name'] for m in models]}")
                
                # 检查所需模型是否存在
                model_names = [m['name'] for m in models]
                if self.model not in model_names:
                    self.logger.warning(f"指定的模型 {self.model} 不在可用模型列表中")
                    return False
                return True
            else:
                self.logger.error(f"Ollama连接测试失败: {response.status_code}")
                return False
        except Exception as e:
            self.logger.error(f"无法连接到Ollama: {str(e)}")
            return False