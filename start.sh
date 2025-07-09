#!/bin/bash

# AI识别总结工具启动脚本

echo "🚀 启动AI识别总结工具..."

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "❌ 虚拟环境不存在，请先运行 ./install.sh"
    exit 1
fi

# 激活虚拟环境
source venv/bin/activate

# 检查Ollama服务
if ! curl -s http://localhost:11434/api/tags &> /dev/null; then
    echo "🔄 启动Ollama服务..."
    brew services start ollama
    sleep 5
    
    # 如果服务仍未启动，尝试手动启动
    if ! curl -s http://localhost:11434/api/tags &> /dev/null; then
        echo "🔧 手动启动Ollama..."
        ollama serve &
        sleep 10
    fi
fi

# 检查配置文件
if [ ! -f "config.yaml" ]; then
    echo "❌ 配置文件不存在"
    exit 1
fi

# 创建PID文件目录
mkdir -p /tmp/activity_tracker

# 启动主程序
echo "✅ 启动活动追踪器..."
python3 main.py &

# 保存PID
echo $! > /tmp/activity_tracker/activity_tracker.pid

echo "🎉 AI识别总结工具已启动！"
echo "📝 日志文件: activity_tracker.log"
echo "🛑 停止程序: ./stop.sh"
echo "📊 查看统计: python3 main.py --stats"