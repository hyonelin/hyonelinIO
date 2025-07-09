#!/bin/bash

# AI识别总结工具停止脚本

echo "🛑 停止AI识别总结工具..."

PID_FILE="/tmp/activity_tracker/activity_tracker.pid"

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    
    if kill -0 "$PID" 2>/dev/null; then
        echo "📊 正在停止进程 $PID..."
        kill -TERM "$PID"
        
        # 等待进程优雅退出
        for i in {1..10}; do
            if ! kill -0 "$PID" 2>/dev/null; then
                echo "✅ 进程已优雅退出"
                break
            fi
            sleep 1
        done
        
        # 如果进程仍在运行，强制终止
        if kill -0 "$PID" 2>/dev/null; then
            echo "⚠️  强制终止进程..."
            kill -KILL "$PID"
        fi
    else
        echo "❌ 进程 $PID 不存在"
    fi
    
    # 删除PID文件
    rm -f "$PID_FILE"
else
    echo "❌ PID文件不存在，尝试查找运行中的进程..."
    
    # 查找并终止Python主程序
    PIDS=$(pgrep -f "python3 main.py")
    if [ ! -z "$PIDS" ]; then
        echo "📊 找到运行中的进程: $PIDS"
        for pid in $PIDS; do
            echo "🛑 终止进程 $pid"
            kill -TERM "$pid"
        done
        sleep 2
        
        # 检查是否还有进程运行
        REMAINING_PIDS=$(pgrep -f "python3 main.py")
        if [ ! -z "$REMAINING_PIDS" ]; then
            echo "⚠️  强制终止剩余进程..."
            for pid in $REMAINING_PIDS; do
                kill -KILL "$pid"
            done
        fi
    else
        echo "❌ 未找到运行中的AI识别总结工具进程"
    fi
fi

echo "✅ AI识别总结工具已停止"