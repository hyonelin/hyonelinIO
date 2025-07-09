#!/bin/bash

# Build script for macOS app packaging
# This script builds the app and creates a DMG file

set -e

APP_NAME="AI活动追踪器"
APP_VERSION="1.0.0"
BUILD_DIR="build"
DIST_DIR="dist"
DMG_NAME="AI活动追踪器-${APP_VERSION}.dmg"

echo "🚀 开始构建 macOS 应用程序..."

# 清理之前的构建
echo "🧹 清理构建目录..."
rm -rf "$BUILD_DIR"
rm -rf "$DIST_DIR"

# 检查依赖
echo "📦 检查依赖..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 未安装"
    exit 1
fi

# 安装构建依赖
echo "🔧 安装构建依赖..."
pip3 install py2app
pip3 install -r requirements.txt

# 构建应用程序
echo "🏗️ 构建应用程序..."
python3 setup.py py2app

# 检查构建是否成功
if [ ! -d "$DIST_DIR/$APP_NAME.app" ]; then
    echo "❌ 应用程序构建失败"
    exit 1
fi

echo "✅ 应用程序构建成功: $DIST_DIR/$APP_NAME.app"

# 创建DMG文件
echo "📦 创建DMG安装包..."

# 创建临时目录
DMG_TEMP_DIR="dmg_temp"
rm -rf "$DMG_TEMP_DIR"
mkdir -p "$DMG_TEMP_DIR"

# 复制应用到临时目录
cp -R "$DIST_DIR/$APP_NAME.app" "$DMG_TEMP_DIR/"

# 创建Applications快捷方式
ln -sf /Applications "$DMG_TEMP_DIR/Applications"

# 创建DMG文件
if command -v hdiutil &> /dev/null; then
    hdiutil create -volname "$APP_NAME" -srcfolder "$DMG_TEMP_DIR" -ov -format UDZO "$DIST_DIR/$DMG_NAME"
    echo "✅ DMG文件创建成功: $DIST_DIR/$DMG_NAME"
else
    echo "⚠️ hdiutil 命令不可用，跳过DMG创建"
fi

# 清理临时目录
rm -rf "$DMG_TEMP_DIR"

# 显示构建结果
echo ""
echo "🎉 构建完成！"
echo "📁 应用程序位置: $DIST_DIR/$APP_NAME.app"
if [ -f "$DIST_DIR/$DMG_NAME" ]; then
    echo "📦 DMG文件位置: $DIST_DIR/$DMG_NAME"
fi
echo ""
echo "💡 使用说明："
echo "1. 双击 $APP_NAME.app 直接运行应用"
echo "2. 或安装DMG文件到Applications目录"
echo "3. 首次运行需要在系统偏好设置中授予屏幕录制权限"
echo ""

# 获取应用大小
if [ -d "$DIST_DIR/$APP_NAME.app" ]; then
    APP_SIZE=$(du -sh "$DIST_DIR/$APP_NAME.app" | cut -f1)
    echo "📊 应用大小: $APP_SIZE"
fi

if [ -f "$DIST_DIR/$DMG_NAME" ]; then
    DMG_SIZE=$(du -sh "$DIST_DIR/$DMG_NAME" | cut -f1)
    echo "📊 DMG大小: $DMG_SIZE"
fi

echo ""
echo "🔍 测试应用程序..."
echo "可以通过以下命令测试："
echo "open '$DIST_DIR/$APP_NAME.app'"