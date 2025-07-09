# 创建应用图标

## 快速创建图标

1. 准备一个 1024x1024 的 PNG 图片作为应用图标
2. 使用以下命令创建 icns 文件：

```bash
# 创建图标集目录
mkdir AI活动追踪器.iconset

# 创建不同尺寸的图标
sips -z 16 16     icon.png --out AI活动追踪器.iconset/icon_16x16.png
sips -z 32 32     icon.png --out AI活动追踪器.iconset/icon_16x16@2x.png
sips -z 32 32     icon.png --out AI活动追踪器.iconset/icon_32x32.png
sips -z 64 64     icon.png --out AI活动追踪器.iconset/icon_32x32@2x.png
sips -z 128 128   icon.png --out AI活动追踪器.iconset/icon_128x128.png
sips -z 256 256   icon.png --out AI活动追踪器.iconset/icon_128x128@2x.png
sips -z 256 256   icon.png --out AI活动追踪器.iconset/icon_256x256.png
sips -z 512 512   icon.png --out AI活动追踪器.iconset/icon_256x256@2x.png
sips -z 512 512   icon.png --out AI活动追踪器.iconset/icon_512x512.png
sips -z 1024 1024 icon.png --out AI活动追踪器.iconset/icon_512x512@2x.png

# 创建 icns 文件
iconutil -c icns AI活动追踪器.iconset

# 移动到 assets 目录
mv AI活动追踪器.icns assets/icon.icns

# 清理临时文件
rm -rf AI活动追踪器.iconset
```

## 或者使用在线工具

1. 访问 https://iconverticons.com/online/
2. 上传你的 PNG 图片
3. 选择转换为 ICNS 格式
4. 下载并重命名为 `icon.icns`
5. 放入 `assets` 目录

## 默认图标

如果没有自定义图标，应用程序会使用 Python 的默认图标。