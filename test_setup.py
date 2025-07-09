#!/usr/bin/env python3
"""
系统设置测试脚本
验证AI识别总结工具的各项依赖是否正确安装和配置
"""

import os
import sys
import yaml
import requests
import subprocess
from datetime import datetime

def test_python_version():
    """测试Python版本"""
    print("🐍 测试Python版本...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python版本: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python版本过低: {version.major}.{version.minor}.{version.micro} (需要3.8+)")
        return False

def test_dependencies():
    """测试Python依赖"""
    print("📦 测试Python依赖...")
    required_modules = ['yaml', 'requests', 'schedule', 'PIL']
    missing = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"  ✅ {module}")
        except ImportError:
            print(f"  ❌ {module}")
            missing.append(module)
    
    if missing:
        print(f"❌ 缺少依赖: {', '.join(missing)}")
        print("请运行: pip install -r requirements.txt")
        return False
    
    print("✅ 所有Python依赖都已安装")
    return True

def test_ollama_connection():
    """测试Ollama连接"""
    print("🤖 测试Ollama连接...")
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            print(f"✅ Ollama连接成功，发现{len(models)}个模型")
            
            # 检查所需模型
            model_names = [m['name'] for m in models]
            required_models = ['llava:latest', 'llama2:latest']
            missing_models = []
            
            for model in required_models:
                if any(model in name for name in model_names):
                    print(f"  ✅ {model}")
                else:
                    print(f"  ❌ {model}")
                    missing_models.append(model)
            
            if missing_models:
                print("❌ 缺少必要的AI模型")
                print("请运行以下命令下载模型:")
                for model in missing_models:
                    print(f"  ollama pull {model}")
                return False
            
            return True
        else:
            print(f"❌ Ollama服务响应错误: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到Ollama服务")
        print("请确保Ollama正在运行: brew services start ollama")
        return False
    except Exception as e:
        print(f"❌ Ollama测试失败: {str(e)}")
        return False

def test_screenshot_capability():
    """测试截图功能"""
    print("📸 测试截图功能...")
    try:
        # 尝试使用screencapture命令
        result = subprocess.run([
            'screencapture', '-x', '-T', '1', '/tmp/test_screenshot.png'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            if os.path.exists('/tmp/test_screenshot.png'):
                print("✅ 截图功能正常")
                os.remove('/tmp/test_screenshot.png')
                return True
            else:
                print("❌ 截图文件未生成")
                return False
        else:
            print(f"❌ 截图命令失败: {result.stderr}")
            print("请在系统偏好设置中为终端添加屏幕录制权限")
            return False
    except Exception as e:
        print(f"❌ 截图测试失败: {str(e)}")
        return False

def test_config_file():
    """测试配置文件"""
    print("⚙️ 测试配置文件...")
    if not os.path.exists('config.yaml'):
        print("❌ 配置文件不存在")
        return False
    
    try:
        with open('config.yaml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        required_sections = ['ollama', 'screenshot', 'storage', 'analysis', 'summary']
        missing_sections = []
        
        for section in required_sections:
            if section in config:
                print(f"  ✅ {section}")
            else:
                print(f"  ❌ {section}")
                missing_sections.append(section)
        
        if missing_sections:
            print(f"❌ 配置文件缺少必要部分: {', '.join(missing_sections)}")
            return False
        
        print("✅ 配置文件格式正确")
        return True
    except Exception as e:
        print(f"❌ 配置文件解析失败: {str(e)}")
        return False

def test_data_directory():
    """测试数据目录"""
    print("📁 测试数据目录...")
    try:
        os.makedirs('data/screenshots', exist_ok=True)
        
        # 测试写入权限
        test_file = 'data/test_write.txt'
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
        
        print("✅ 数据目录权限正常")
        return True
    except Exception as e:
        print(f"❌ 数据目录测试失败: {str(e)}")
        return False

def main():
    """主测试函数"""
    print("🧪 AI识别总结工具系统测试")
    print("=" * 50)
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        test_python_version,
        test_dependencies,
        test_config_file,
        test_data_directory,
        test_ollama_connection,
        test_screenshot_capability
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            print()
        except Exception as e:
            print(f"❌ 测试异常: {str(e)}")
            print()
    
    print("=" * 50)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！系统准备就绪")
        print("可以运行 ./start.sh 启动活动追踪器")
        return True
    else:
        print("⚠️  部分测试失败，请根据上述提示进行修复")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)