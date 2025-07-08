#!/bin/bash

# AI识别总结工具安装脚本 - macOS版本

set -e

echo "🚀 开始安装AI识别总结工具..."

# 检查系统
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ 此脚本仅支持macOS系统"
    exit 1
fi

# 检查Python版本
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python3，请先安装Python3"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.8"

if [[ $(echo "$PYTHON_VERSION < $REQUIRED_VERSION" | bc -l) -eq 1 ]]; then
    echo "❌ Python版本过低，需要Python 3.8+，当前版本: $PYTHON_VERSION"
    exit 1
fi

echo "✅ Python版本检查通过: $PYTHON_VERSION"

# 检查Homebrew
if ! command -v brew &> /dev/null; then
    echo "📦 安装Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# 检查并安装Ollama
if ! command -v ollama &> /dev/null; then
    echo "📦 安装Ollama..."
    brew install ollama
else
    echo "✅ Ollama已安装"
fi

# 启动Ollama服务
echo "🔄 启动Ollama服务..."
brew services start ollama

# 等待Ollama服务启动
echo "⏳ 等待Ollama服务启动..."
sleep 5

# 检查Ollama服务状态
if ! curl -s http://localhost:11434/api/tags &> /dev/null; then
    echo "⚠️  Ollama服务可能未完全启动，手动启动中..."
    ollama serve &
    sleep 10
fi

# 下载llava模型
echo "📥 下载llava视觉分析模型（这可能需要几分钟）..."
ollama pull llava:latest

echo "📥 下载llama2文本模型用于总结生成..."
ollama pull llama2:latest

# 创建虚拟环境
echo "🐍 创建Python虚拟环境..."
python3 -m venv venv
source venv/bin/activate

# 安装Python依赖
echo "📦 安装Python依赖..."
pip install --upgrade pip
pip install -r requirements.txt

# 创建必要的目录
echo "📁 创建数据目录..."
mkdir -p data/screenshots

# 创建日志文件
touch activity_tracker.log

# 设置权限
echo "🔒 设置文件权限..."
chmod +x main.py
chmod +x start.sh
chmod +x stop.sh

echo ""
echo "🎉 安装完成！"
echo ""
echo "📝 重要提示："
echo "1. 请在 系统偏好设置 > 安全性与隐私 > 隐私 > 屏幕录制 中"
echo "   为终端应用添加权限"
echo ""
echo "2. 确保Ollama服务正在运行："
echo "   brew services start ollama"
echo ""
echo "3. 启动活动追踪器："
echo "   ./start.sh"
echo ""
echo "4. 查看帮助："
echo "   python3 main.py --help"
echo ""
echo "5. 查看统计信息："
echo "   python3 main.py --stats"
echo ""

# 测试安装
echo "🧪 测试安装..."
source venv/bin/activate
if python3 -c "import yaml, schedule, requests, PIL; print('✅ 所有依赖模块导入成功')"; then
    echo "✅ 安装测试通过"
else
    echo "❌ 安装测试失败，请检查依赖"
    exit 1
fi

echo "🎯 安装脚本执行完成！"