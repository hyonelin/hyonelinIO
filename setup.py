"""
Setup script for building macOS app with py2app
"""

from setuptools import setup
import os

# py2app will be imported at runtime
try:
    import py2app  # type: ignore
except ImportError:
    py2app = None

# App name and version
APP_NAME = "AI活动追踪器"
APP_VERSION = "1.0.0"

# Main entry point
APP_SCRIPT = "src/gui_app.py"

# Icon file (if available)
ICON_FILE = "assets/icon.icns"  # You can create this later

# Include all necessary files (proper format for setuptools)
DATA_FILES = [
    (".", ["config.yaml", "requirements.txt", "README.md"]),
    ("src", ["src/__init__.py", "src/database_manager.py", "src/ollama_client.py", "src/screenshot_capture.py", "src/gui_app.py"]),
]

# Python modules to include
PACKAGES = [
    'tkinter',
    'yaml',
    'PIL',
    'requests',
    'schedule',
    'sqlite3',
    'threading',
    'datetime',
    'os',
    'sys',
    'time',
    'logging',
    'signal',
    'base64',
    'json',
    'subprocess',
]

# App configuration
APP_OPTIONS = {
    'argv_emulation': True,
    'iconfile': ICON_FILE if os.path.exists(ICON_FILE) else None,
    'plist': {
        'CFBundleName': APP_NAME,
        'CFBundleDisplayName': APP_NAME,
        'CFBundleIdentifier': 'com.aitools.activitytracker',
        'CFBundleVersion': APP_VERSION,
        'CFBundleShortVersionString': APP_VERSION,
        'NSHumanReadableCopyright': '© 2024 AI Activity Tracker',
        'NSHighResolutionCapable': True,
        'LSUIElement': False,  # Set to True if you want to hide from dock
        'NSRequiresAquaSystemAppearance': False,
        'NSCameraUsageDescription': 'This app needs camera access for screenshot capture.',
        'NSScreenCaptureDescription': 'This app needs screen recording access to capture screenshots for activity analysis.',
        'NSMicrophoneUsageDescription': 'This app may need microphone access for enhanced analysis.',
    },
    'resources': DATA_FILES,
    'includes': [
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'yaml',
        'PIL',
        'PIL.Image',
        'PIL.ImageGrab',
        'requests',
        'schedule',
        'sqlite3',
        'threading',
        'datetime',
        'base64',
        'json',
        'subprocess',
        'logging',
        'signal',
    ],
    'excludes': [
        'numpy',
        'scipy',
        'matplotlib',
        'pandas',
    ],
    'strip': True,
    'optimize': 2,
}

# Build options
OPTIONS = {
    'py2app': APP_OPTIONS,
    'build_exe': {
        'packages': PACKAGES,
        'includes': [],
        'excludes': ['numpy', 'scipy', 'matplotlib', 'pandas'],
        'include_files': DATA_FILES,
    }
}

setup(
    name=APP_NAME,
    version=APP_VERSION,
    description="AI-powered activity tracking and analysis tool",
    author="AI Assistant",
    app=[APP_SCRIPT],
    data_files=DATA_FILES,
    options=OPTIONS,
    setup_requires=['py2app'],
    install_requires=[
        'Pillow>=10.0.1',
        'requests>=2.31.0',
        'schedule>=1.2.0',
        'PyYAML>=6.0.1',
        'py2app>=0.28.0',
    ],
)