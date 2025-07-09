#!/usr/bin/env python3
"""
GUI界面主程序
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import sys
import yaml
import threading
import time
from datetime import datetime
import webbrowser

# 添加父目录到路径
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from main import ActivityTracker

class SettingsWindow:
    def __init__(self, parent, config, on_save_callback):
        self.parent = parent
        self.config = config.copy()
        self.on_save_callback = on_save_callback
        
        self.window = tk.Toplevel(parent)
        self.window.title("设置")
        self.window.geometry("600x500")
        self.window.resizable(False, False)
        
        # 设置窗口居中
        self.window.transient(parent)
        self.window.grab_set()
        
        self.create_widgets()
        self.load_current_settings()
        
        # 确保窗口在前面
        self.window.lift()
        self.window.focus_set()
    
    def create_widgets(self):
        # 创建笔记本标签页
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 基本设置页
        basic_frame = ttk.Frame(notebook)
        notebook.add(basic_frame, text="基本设置")
        
        # AI设置页
        ai_frame = ttk.Frame(notebook)
        notebook.add(ai_frame, text="AI设置")
        
        # 存储设置页
        storage_frame = ttk.Frame(notebook)
        notebook.add(storage_frame, text="存储设置")
        
        # 创建基本设置
        self.create_basic_settings(basic_frame)
        
        # 创建AI设置
        self.create_ai_settings(ai_frame)
        
        # 创建存储设置
        self.create_storage_settings(storage_frame)
        
        # 按钮框架
        button_frame = ttk.Frame(self.window)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Button(button_frame, text="保存", command=self.save_settings).pack(side="right", padx=5)
        ttk.Button(button_frame, text="取消", command=self.window.destroy).pack(side="right", padx=5)
        ttk.Button(button_frame, text="恢复默认", command=self.restore_defaults).pack(side="left", padx=5)
    
    def create_basic_settings(self, parent):
        # 截图设置
        screenshot_frame = ttk.LabelFrame(parent, text="截图设置", padding=10)
        screenshot_frame.pack(fill="x", pady=5)
        
        # 截图间隔
        ttk.Label(screenshot_frame, text="截图间隔（分钟）:").grid(row=0, column=0, sticky="w")
        self.interval_var = tk.StringVar()
        ttk.Entry(screenshot_frame, textvariable=self.interval_var, width=10).grid(row=0, column=1, padx=5)
        
        # 保存截图
        self.save_screenshots_var = tk.BooleanVar()
        ttk.Checkbutton(screenshot_frame, text="保存截图文件", variable=self.save_screenshots_var).grid(row=1, column=0, columnspan=2, sticky="w", pady=5)
        
        # 截图质量
        ttk.Label(screenshot_frame, text="截图质量 (1-100):").grid(row=2, column=0, sticky="w")
        self.quality_var = tk.StringVar()
        ttk.Entry(screenshot_frame, textvariable=self.quality_var, width=10).grid(row=2, column=1, padx=5)
        
        # 总结设置
        summary_frame = ttk.LabelFrame(parent, text="总结设置", padding=10)
        summary_frame.pack(fill="x", pady=5)
        
        # 每日总结时间
        ttk.Label(summary_frame, text="每日总结时间:").grid(row=0, column=0, sticky="w")
        self.summary_time_var = tk.StringVar()
        ttk.Entry(summary_frame, textvariable=self.summary_time_var, width=10).grid(row=0, column=1, padx=5)
        ttk.Label(summary_frame, text="(格式: HH:MM)").grid(row=0, column=2, sticky="w")
    
    def create_ai_settings(self, parent):
        # Ollama设置
        ollama_frame = ttk.LabelFrame(parent, text="Ollama设置", padding=10)
        ollama_frame.pack(fill="x", pady=5)
        
        # 基础URL
        ttk.Label(ollama_frame, text="Ollama URL:").grid(row=0, column=0, sticky="w")
        self.ollama_url_var = tk.StringVar()
        ttk.Entry(ollama_frame, textvariable=self.ollama_url_var, width=40).grid(row=0, column=1, padx=5)
        
        # 模型名称
        ttk.Label(ollama_frame, text="模型名称:").grid(row=1, column=0, sticky="w")
        self.model_var = tk.StringVar()
        ttk.Entry(ollama_frame, textvariable=self.model_var, width=40).grid(row=1, column=1, padx=5)
        
        # 超时设置
        ttk.Label(ollama_frame, text="超时时间（秒）:").grid(row=2, column=0, sticky="w")
        self.timeout_var = tk.StringVar()
        ttk.Entry(ollama_frame, textvariable=self.timeout_var, width=10).grid(row=2, column=1, padx=5)
        
        # 分析提示词
        analysis_frame = ttk.LabelFrame(parent, text="分析提示词", padding=10)
        analysis_frame.pack(fill="both", expand=True, pady=5)
        
        self.analysis_prompt_text = tk.Text(analysis_frame, height=6, wrap=tk.WORD)
        self.analysis_prompt_text.pack(fill="both", expand=True)
        
        # 总结提示词
        summary_prompt_frame = ttk.LabelFrame(parent, text="总结提示词", padding=10)
        summary_prompt_frame.pack(fill="both", expand=True, pady=5)
        
        self.summary_prompt_text = tk.Text(summary_prompt_frame, height=6, wrap=tk.WORD)
        self.summary_prompt_text.pack(fill="both", expand=True)
    
    def create_storage_settings(self, parent):
        # 存储路径设置
        storage_frame = ttk.LabelFrame(parent, text="存储路径", padding=10)
        storage_frame.pack(fill="x", pady=5)
        
        # 数据目录
        ttk.Label(storage_frame, text="数据目录:").grid(row=0, column=0, sticky="w")
        self.data_dir_var = tk.StringVar()
        ttk.Entry(storage_frame, textvariable=self.data_dir_var, width=40).grid(row=0, column=1, padx=5)
        ttk.Button(storage_frame, text="浏览", command=self.browse_data_dir).grid(row=0, column=2, padx=5)
        
        # 数据库文件
        ttk.Label(storage_frame, text="数据库文件:").grid(row=1, column=0, sticky="w")
        self.database_var = tk.StringVar()
        ttk.Entry(storage_frame, textvariable=self.database_var, width=40).grid(row=1, column=1, padx=5)
        ttk.Button(storage_frame, text="浏览", command=self.browse_database).grid(row=1, column=2, padx=5)
        
        # 截图目录
        ttk.Label(storage_frame, text="截图目录:").grid(row=2, column=0, sticky="w")
        self.screenshots_dir_var = tk.StringVar()
        ttk.Entry(storage_frame, textvariable=self.screenshots_dir_var, width=40).grid(row=2, column=1, padx=5)
        ttk.Button(storage_frame, text="浏览", command=self.browse_screenshots_dir).grid(row=2, column=2, padx=5)
    
    def browse_data_dir(self):
        directory = filedialog.askdirectory()
        if directory:
            self.data_dir_var.set(directory)
    
    def browse_database(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".db",
            filetypes=[("Database files", "*.db"), ("All files", "*.*")]
        )
        if filename:
            self.database_var.set(filename)
    
    def browse_screenshots_dir(self):
        directory = filedialog.askdirectory()
        if directory:
            self.screenshots_dir_var.set(directory)
    
    def load_current_settings(self):
        # 加载基本设置
        self.interval_var.set(str(self.config.get('screenshot', {}).get('interval_minutes', 1)))
        self.save_screenshots_var.set(self.config.get('screenshot', {}).get('save_screenshots', True))
        self.quality_var.set(str(self.config.get('screenshot', {}).get('screenshot_quality', 85)))
        self.summary_time_var.set(self.config.get('summary', {}).get('daily_summary_time', '23:30'))
        
        # 加载AI设置
        self.ollama_url_var.set(self.config.get('ollama', {}).get('base_url', 'http://localhost:11434'))
        self.model_var.set(self.config.get('ollama', {}).get('model', 'llava:latest'))
        self.timeout_var.set(str(self.config.get('ollama', {}).get('timeout', 30)))
        
        # 加载提示词
        analysis_prompt = self.config.get('analysis', {}).get('system_prompt', '')
        self.analysis_prompt_text.delete(1.0, tk.END)
        self.analysis_prompt_text.insert(1.0, analysis_prompt)
        
        summary_prompt = self.config.get('summary', {}).get('summary_prompt', '')
        self.summary_prompt_text.delete(1.0, tk.END)
        self.summary_prompt_text.insert(1.0, summary_prompt)
        
        # 加载存储设置
        self.data_dir_var.set(self.config.get('storage', {}).get('data_dir', './data'))
        self.database_var.set(self.config.get('storage', {}).get('database', './data/activity_log.db'))
        self.screenshots_dir_var.set(self.config.get('storage', {}).get('screenshots_dir', './data/screenshots'))
    
    def save_settings(self):
        try:
            # 验证输入
            interval = int(self.interval_var.get())
            if interval < 1:
                raise ValueError("截图间隔必须大于0")
            
            quality = int(self.quality_var.get())
            if not (1 <= quality <= 100):
                raise ValueError("截图质量必须在1-100之间")
            
            timeout = int(self.timeout_var.get())
            if timeout < 1:
                raise ValueError("超时时间必须大于0")
            
            # 验证时间格式
            time_str = self.summary_time_var.get()
            datetime.strptime(time_str, "%H:%M")
            
            # 更新配置
            self.config['screenshot'] = {
                'interval_minutes': interval,
                'save_screenshots': self.save_screenshots_var.get(),
                'screenshot_quality': quality
            }
            
            self.config['summary'] = {
                'daily_summary_time': time_str,
                'summary_prompt': self.summary_prompt_text.get(1.0, tk.END).strip()
            }
            
            self.config['ollama'] = {
                'base_url': self.ollama_url_var.get(),
                'model': self.model_var.get(),
                'timeout': timeout
            }
            
            self.config['analysis'] = {
                'system_prompt': self.analysis_prompt_text.get(1.0, tk.END).strip()
            }
            
            self.config['storage'] = {
                'data_dir': self.data_dir_var.get(),
                'database': self.database_var.get(),
                'screenshots_dir': self.screenshots_dir_var.get()
            }
            
            # 保存配置
            self.on_save_callback(self.config)
            messagebox.showinfo("成功", "设置已保存")
            self.window.destroy()
            
        except ValueError as e:
            messagebox.showerror("输入错误", str(e))
        except Exception as e:
            messagebox.showerror("保存失败", f"保存配置时出错: {str(e)}")
    
    def restore_defaults(self):
        if messagebox.askyesno("确认", "确定要恢复默认设置吗？"):
            # 恢复默认配置
            default_config = {
                'ollama': {
                    'base_url': 'http://localhost:11434',
                    'model': 'llava:latest',
                    'timeout': 30
                },
                'screenshot': {
                    'interval_minutes': 1,
                    'save_screenshots': True,
                    'screenshot_quality': 85
                },
                'storage': {
                    'data_dir': './data',
                    'database': './data/activity_log.db',
                    'screenshots_dir': './data/screenshots'
                },
                'analysis': {
                    'system_prompt': '''你是一个专业的屏幕内容分析助手。请仔细观察这张屏幕截图，识别用户正在进行的活动。
请用简洁的中文描述用户在做什么，包括：
1. 正在使用的应用程序或网站
2. 正在进行的具体活动
3. 活动的主要内容或目的

请只回答关键信息，不要添加多余的解释。'''
                },
                'summary': {
                    'daily_summary_time': '23:30',
                    'summary_prompt': '''请根据以下一天的活动记录，生成一份简洁的中文总结报告。
总结应该包括：
1. 主要工作内容和时间分配
2. 使用的主要应用程序和工具
3. 学习或娱乐活动
4. 工作效率评估和建议

请用条理清晰的格式呈现，重点突出有价值的信息。'''
                }
            }
            
            self.config = default_config
            self.load_current_settings()

class ActivityTrackerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AI活动追踪器")
        self.root.geometry("800x600")
        
        # 设置窗口图标（如果有的话）
        # self.root.iconbitmap("icon.ico")
        
        self.tracker = None
        self.tracker_thread = None
        self.running = False
        
        # 加载配置
        self.config_path = "config.yaml"
        self.config = self.load_config()
        
        self.create_widgets()
        self.setup_menu()
        
        # 定期更新状态
        self.update_status()
        
        # 处理窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def load_config(self):
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            messagebox.showerror("错误", f"加载配置失败: {str(e)}")
            return {}
    
    def save_config(self, config):
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
            self.config = config
            messagebox.showinfo("成功", "配置已保存")
        except Exception as e:
            messagebox.showerror("错误", f"保存配置失败: {str(e)}")
    
    def setup_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="设置", command=self.open_settings)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.on_closing)
        
        # 查看菜单
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="查看", menu=view_menu)
        view_menu.add_command(label="活动统计", command=self.show_stats)
        view_menu.add_command(label="今日总结", command=self.show_today_summary)
        
        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="帮助", menu=help_menu)
        help_menu.add_command(label="关于", command=self.show_about)
    
    def create_widgets(self):
        # 主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 状态框架
        status_frame = ttk.LabelFrame(main_frame, text="状态", padding=10)
        status_frame.pack(fill="x", pady=5)
        
        # 状态标签
        self.status_label = ttk.Label(status_frame, text="未运行", foreground="red")
        self.status_label.pack(side="left")
        
        # 最后活动时间
        self.last_activity_label = ttk.Label(status_frame, text="")
        self.last_activity_label.pack(side="right")
        
        # 控制按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=5)
        
        self.start_button = ttk.Button(button_frame, text="开始追踪", command=self.start_tracking)
        self.start_button.pack(side="left", padx=5)
        
        self.stop_button = ttk.Button(button_frame, text="停止追踪", command=self.stop_tracking, state="disabled")
        self.stop_button.pack(side="left", padx=5)
        
        ttk.Button(button_frame, text="设置", command=self.open_settings).pack(side="left", padx=5)
        
        ttk.Button(button_frame, text="生成总结", command=self.generate_summary).pack(side="right", padx=5)
        ttk.Button(button_frame, text="查看统计", command=self.show_stats).pack(side="right", padx=5)
        
        # 日志框架
        log_frame = ttk.LabelFrame(main_frame, text="活动日志", padding=10)
        log_frame.pack(fill="both", expand=True, pady=5)
        
        # 创建日志文本区域
        self.log_text = tk.Text(log_frame, height=20, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 配置信息框架
        config_frame = ttk.LabelFrame(main_frame, text="当前配置", padding=10)
        config_frame.pack(fill="x", pady=5)
        
        self.config_label = ttk.Label(config_frame, text="")
        self.config_label.pack(anchor="w")
        
        self.update_config_display()
    
    def update_config_display(self):
        config_text = f"截图间隔: {self.config.get('screenshot', {}).get('interval_minutes', 1)}分钟 | "
        config_text += f"Ollama: {self.config.get('ollama', {}).get('base_url', 'N/A')} | "
        config_text += f"模型: {self.config.get('ollama', {}).get('model', 'N/A')}"
        self.config_label.config(text=config_text)
    
    def start_tracking(self):
        if not self.running:
            try:
                self.tracker = ActivityTracker(self.config_path)
                
                # 在后台线程中运行追踪器
                self.tracker_thread = threading.Thread(target=self.run_tracker, daemon=True)
                self.tracker_thread.start()
                
                self.running = True
                self.start_button.config(state="disabled")
                self.stop_button.config(state="normal")
                self.status_label.config(text="运行中", foreground="green")
                
                self.log_message("✅ 追踪器已启动")
                
            except Exception as e:
                messagebox.showerror("启动失败", f"启动追踪器时出错: {str(e)}")
                self.log_message(f"❌ 启动失败: {str(e)}")
    
    def stop_tracking(self):
        if self.running and self.tracker:
            self.running = False
            self.tracker.running = False
            self.tracker.stop_event.set()
            
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
            self.status_label.config(text="未运行", foreground="red")
            
            self.log_message("🛑 追踪器已停止")
    
    def run_tracker(self):
        try:
            if self.tracker is not None:
                self.tracker.start()
        except Exception as e:
            self.log_message(f"❌ 追踪器运行出错: {str(e)}")
            self.running = False
            self.root.after(0, lambda: self.start_button.config(state="normal"))
            self.root.after(0, lambda: self.stop_button.config(state="disabled"))
            self.root.after(0, lambda: self.status_label.config(text="运行出错", foreground="red"))
    
    def log_message(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        # 在主线程中更新GUI
        self.root.after(0, lambda: self._update_log(log_entry))
    
    def _update_log(self, log_entry):
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        
        # 限制日志条目数量
        lines = self.log_text.get(1.0, tk.END).split('\n')
        if len(lines) > 100:
            self.log_text.delete(1.0, f"{len(lines) - 100}.0")
    
    def update_status(self):
        # 更新最后活动时间
        if self.running:
            self.last_activity_label.config(text=f"最后更新: {datetime.now().strftime('%H:%M:%S')}")
        
        # 每秒更新一次
        self.root.after(1000, self.update_status)
    
    def open_settings(self):
        SettingsWindow(self.root, self.config, self.save_config)
        self.update_config_display()
    
    def show_stats(self):
        # 显示统计信息窗口
        stats_window = tk.Toplevel(self.root)
        stats_window.title("活动统计")
        stats_window.geometry("600x400")
        
        text_widget = tk.Text(stats_window, wrap=tk.WORD, padx=10, pady=10)
        text_widget.pack(fill="both", expand=True)
        
        # 获取统计信息
        try:
            if self.tracker:
                stats = self.tracker.db_manager.get_activity_stats()
                if stats:
                    stats_text = f"""📈 活动统计
={'='*40}
📅 统计周期: 最近{stats['period_days']}天
📊 总活动次数: {stats['total_activities']}
🗓️ 活跃天数: {stats['active_days']}
📈 日均活动: {stats['avg_activities_per_day']}
"""
                    if stats['most_active_day']:
                        stats_text += f"🔥 最活跃日期: {stats['most_active_day']} ({stats['most_active_day_count']}次)"
                    
                    text_widget.insert(tk.END, stats_text)
                else:
                    text_widget.insert(tk.END, "暂无统计数据")
            else:
                text_widget.insert(tk.END, "请先启动追踪器")
        except Exception as e:
            text_widget.insert(tk.END, f"获取统计信息失败: {str(e)}")
    
    def show_today_summary(self):
        # 显示今日总结窗口
        summary_window = tk.Toplevel(self.root)
        summary_window.title("今日总结")
        summary_window.geometry("600x400")
        
        text_widget = tk.Text(summary_window, wrap=tk.WORD, padx=10, pady=10)
        text_widget.pack(fill="both", expand=True)
        
        # 获取今日总结
        try:
            if self.tracker:
                from datetime import date
                today = date.today()
                summary = self.tracker.db_manager.get_daily_summary(today)
                if summary:
                    summary_text = f"""📋 今日总结 ({today})
={'='*40}
{summary['summary']}
"""
                    text_widget.insert(tk.END, summary_text)
                else:
                    text_widget.insert(tk.END, "今日暂无总结")
            else:
                text_widget.insert(tk.END, "请先启动追踪器")
        except Exception as e:
            text_widget.insert(tk.END, f"获取今日总结失败: {str(e)}")
    
    def generate_summary(self):
        if self.tracker:
            try:
                threading.Thread(target=self.tracker.generate_daily_summary, daemon=True).start()
                self.log_message("📊 开始生成今日总结...")
                messagebox.showinfo("提示", "总结生成中，请稍候...")
            except Exception as e:
                messagebox.showerror("错误", f"生成总结失败: {str(e)}")
        else:
            messagebox.showwarning("提示", "请先启动追踪器")
    
    def show_about(self):
        about_text = """AI活动追踪器
        
版本: 1.0.0
作者: AI助手

这是一个基于本地Ollama的离线屏幕活动分析和总结工具。

功能特点:
• 定时截图分析
• AI智能识别活动内容
• 自动生成每日总结
• 本地存储，保护隐私
• 可自定义配置

使用前请确保:
1. 已安装并启动Ollama
2. 已下载llava模型
3. 已授权屏幕录制权限
"""
        messagebox.showinfo("关于", about_text)
    
    def on_closing(self):
        if self.running:
            if messagebox.askokcancel("退出", "追踪器正在运行，确定要退出吗？"):
                self.stop_tracking()
                self.root.after(1000, self.root.destroy)  # 等待1秒后关闭
        else:
            self.root.destroy()
    
    def run(self):
        self.root.mainloop()

def main():
    app = ActivityTrackerGUI()
    app.run()

if __name__ == "__main__":
    main()