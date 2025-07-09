# 快速开始指南

## 构建和运行 AI活动追踪器

### 步骤 1：准备环境

确保您的系统满足以下要求：

```bash
# 检查 Python 版本
python3 --version  # 应该是 3.8+

# 检查 Ollama 是否运行
curl http://localhost:11434  # 应该返回 "Ollama is running"

# 下载 llava 模型（如果尚未下载）
ollama pull llava
```

### 步骤 2：构建应用程序

```bash
# 克隆项目（如果需要）
# git clone <your-repo-url>

# 进入项目目录
cd /workspace

# 运行构建脚本
./build_macos.sh
```

### 步骤 3：运行应用程序

构建完成后，您可以通过以下方式运行应用程序：

```bash
# 方式1：直接运行应用程序
open "dist/AI活动追踪器.app"

# 方式2：安装 DMG 文件
open "dist/AI活动追踪器-1.0.0.dmg"
```

### 步骤 4：配置权限

1. 打开 `系统偏好设置` → `安全性与隐私` → `隐私`
2. 选择 `屏幕录制`
3. 添加并勾选 `AI活动追踪器`
4. 重启应用程序

### 步骤 5：开始使用

1. 启动应用程序
2. 点击 "开始追踪" 按钮
3. 通过 "设置" 菜单调整配置
4. 查看实时活动日志

## 测试GUI应用程序

如果您想在构建前测试GUI应用程序：

```bash
# 安装依赖
pip3 install -r requirements.txt

# 运行GUI应用程序
python3 src/gui_app.py
```

## 常见问题

### 构建失败

如果构建过程中遇到问题：

```bash
# 清理并重新构建
rm -rf build dist
./build_macos.sh
```

### 权限问题

如果应用程序无法捕获屏幕：

1. 检查屏幕录制权限是否已授予
2. 尝试重启应用程序
3. 检查 Ollama 服务是否运行

### Ollama 连接问题

```bash
# 检查 Ollama 状态
ollama ps

# 启动 Ollama 服务
ollama serve

# 测试模型
ollama run llava "describe this image" < screenshot.png
```

## 自定义配置

应用程序支持通过设置页面进行配置：

- **截图间隔**：调整分析频率
- **AI模型**：选择不同的 Ollama 模型
- **存储路径**：自定义数据保存位置
- **提示词**：自定义 AI 分析的提示

## 支持

如果您遇到任何问题：

1. 查看 `activity_tracker.log` 日志文件
2. 检查 `APP_BUILD_README.md` 中的故障排除部分
3. 确保所有依赖都已正确安装

---

享受使用 AI活动追踪器！🚀