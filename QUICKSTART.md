# 快速开始指南 🚀

本指南将帮助你在5分钟内在macOS上部署和运行AI识别总结工具。

## 📋 前置要求

- macOS 10.15+ 
- Python 3.8+
- 8GB+ 内存
- 5GB+ 可用磁盘空间

## ⚡ 一键安装

```bash
# 1. 克隆项目并进入目录
git clone <your-repo-url>
cd ai-activity-tracker

# 2. 运行自动安装脚本
./install.sh
```

安装脚本会自动：
- ✅ 安装Homebrew和Ollama
- ✅ 下载AI模型（约8GB）
- ✅ 创建Python环境
- ✅ 安装所有依赖

## 🔐 配置权限

**重要**: 在系统偏好设置中为终端添加屏幕录制权限：

1. 打开 `系统偏好设置` > `安全性与隐私` > `隐私`
2. 选择 `屏幕录制`
3. 点击锁图标并输入密码
4. 勾选 `终端`（或你使用的终端应用）

## 🧪 测试安装

```bash
./test_setup.py
```

确保所有测试都通过 ✅

## 🎯 启动使用

```bash
# 启动活动追踪器
./start.sh

# 查看统计信息（新终端窗口）
source venv/bin/activate
python3 main.py --stats

# 停止追踪器
./stop.sh
```

## 📊 期望效果

启动后，工具将：
- 🔄 每分钟自动截图并分析
- 🧠 使用AI识别你正在做什么
- 📝 记录活动到本地数据库
- 📊 每晚23:30生成总结报告

## ⚙️ 快速配置

编辑 `config.yaml` 调整设置：

```yaml
screenshot:
  interval_minutes: 1    # 改为5可减少频率
  save_screenshots: false  # 设为false可节省空间

summary:
  daily_summary_time: "22:00"  # 改变总结时间
```

## 🆘 常见问题

### Ollama连接失败？
```bash
brew services restart ollama
```

### 截图权限不足？
重新在系统设置中添加权限并重启终端

### 模型下载慢？
耐心等待，模型较大（8GB+）

### 想要节省资源？
设置更长的截图间隔或关闭截图保存

## 📈 查看结果

- **实时日志**: `tail -f activity_tracker.log`
- **今日统计**: `python3 main.py --stats`
- **手动总结**: `python3 main.py --summary`
- **数据库位置**: `data/activity_log.db`

## 🎯 下一步

恭喜！你的AI活动助手已经开始工作了。它会在后台静默运行，分析你的屏幕活动，并在每天结束时为你生成详细的总结报告。

想要更多功能？查看完整的 [README.md](README.md) 文档。