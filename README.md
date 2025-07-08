# AI识别总结工具 🤖

一个基于本地Ollama部署的AI识别总结工具，用于自动分析屏幕活动并生成每日总结报告。**完全离线运行，保护隐私安全**。

## ✨ 功能特点

- 🔄 **自动截屏**: 每分钟自动截取屏幕图片
- 🧠 **AI分析**: 使用本地Ollama的视觉模型分析屏幕内容
- 📊 **智能总结**: 自动生成每日活动总结报告
- 🔒 **隐私保护**: 完全离线运行，数据不上传到云端
- 📁 **本地存储**: 所有数据存储在本地数据库
- ⚙️ **可配置**: 支持自定义截图频率、模型选择等
- 📈 **统计分析**: 提供详细的活动统计信息

## 🛠️ 系统要求

- **操作系统**: macOS 10.15+
- **Python**: 3.8+
- **内存**: 建议8GB+（用于运行AI模型）
- **磁盘空间**: 建议5GB+（用于存储模型和数据）

## 🚀 快速安装

### 1. 克隆项目

```bash
git clone <your-repo-url>
cd ai-activity-tracker
```

### 2. 运行安装脚本

```bash
chmod +x install.sh
./install.sh
```

安装脚本将自动完成以下步骤：
- 安装Homebrew（如果未安装）
- 安装并启动Ollama
- 下载AI模型（llava:latest 和 llama2:latest）
- 创建Python虚拟环境
- 安装所需依赖

### 3. 配置屏幕录制权限

⚠️ **重要**: 在 `系统偏好设置 > 安全性与隐私 > 隐私 > 屏幕录制` 中为终端应用添加权限。

## 🎯 使用方法

### 启动工具

```bash
./start.sh
```

### 停止工具

```bash
./stop.sh
```

### 查看统计信息

```bash
source venv/bin/activate
python3 main.py --stats
```

### 手动生成今日总结

```bash
source venv/bin/activate
python3 main.py --summary
```

## ⚙️ 配置说明

编辑 `config.yaml` 文件来自定义设置：

```yaml
# 截图设置
screenshot:
  interval_minutes: 1        # 截图间隔（分钟）
  save_screenshots: true     # 是否保存截图文件
  screenshot_quality: 85     # 截图质量 (1-100)

# Ollama设置
ollama:
  base_url: "http://localhost:11434"
  model: "llava:latest"      # 视觉分析模型
  timeout: 30                # 请求超时时间

# 总结设置
summary:
  daily_summary_time: "23:30"  # 每日总结生成时间
```

## 📁 项目结构

```
ai-activity-tracker/
├── main.py                 # 主程序
├── config.yaml            # 配置文件
├── requirements.txt       # Python依赖
├── install.sh             # 安装脚本
├── start.sh              # 启动脚本
├── stop.sh               # 停止脚本
├── src/                  # 源代码目录
│   ├── screenshot_capture.py   # 截图模块
│   ├── ollama_client.py        # Ollama客户端
│   └── database_manager.py     # 数据库管理
├── data/                 # 数据目录
│   ├── screenshots/      # 截图存储
│   └── activity_log.db   # 活动数据库
└── activity_tracker.log  # 程序日志
```

## 💾 数据存储

- **活动记录**: 存储在SQLite数据库中（`data/activity_log.db`）
- **截图文件**: 存储在 `data/screenshots/` 目录中
- **日志文件**: 程序运行日志存储在 `activity_tracker.log`

## 📊 功能示例

### 每日总结报告示例

```
==================================================
📊 2024-01-15 每日总结
==================================================

## 主要工作内容
- 代码开发：使用VSCode进行Python项目开发（4小时）
- 文档编写：编写技术文档和README（1.5小时）
- 会议沟通：参加团队会议和讨论（1小时）

## 使用的主要应用
- Visual Studio Code（开发环境）
- Chrome浏览器（查阅文档和搜索）
- Slack（团队沟通）

## 效率分析
- 专注时间：约5.5小时
- 建议：减少浏览器切换，提高专注度
==================================================
```

## 🔧 故障排除

### 1. Ollama连接失败

```bash
# 检查Ollama服务状态
brew services list | grep ollama

# 重启Ollama服务
brew services restart ollama

# 手动启动Ollama
ollama serve
```

### 2. 截图权限问题

- 确保在系统偏好设置中为终端添加了屏幕录制权限
- 重启终端应用程序

### 3. 模型下载问题

```bash
# 重新下载模型
ollama pull llava:latest
ollama pull llama2:latest

# 查看已安装模型
ollama list
```

### 4. Python环境问题

```bash
# 重新创建虚拟环境
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 🛡️ 隐私说明

本工具完全在本地运行，具有以下隐私保护特性：

- ✅ **数据不外传**: 所有截图和分析结果仅存储在本地
- ✅ **离线运行**: 使用本地AI模型，无需连接互联网
- ✅ **用户控制**: 用户完全控制数据的存储和删除
- ✅ **可配置存储**: 可选择是否保存截图文件

## 📝 注意事项

1. **资源消耗**: AI模型运行需要较多CPU和内存资源
2. **磁盘空间**: 长期使用会积累较多数据，建议定期清理
3. **模型大小**: llava模型约4GB，llama2模型约4GB
4. **首次运行**: 首次AI分析可能较慢，后续会逐渐提速

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## 📄 许可证

MIT License

## 📞 支持

如果遇到问题，请查看：
1. 项目日志文件 `activity_tracker.log`
2. 检查Ollama服务状态
3. 验证屏幕录制权限设置