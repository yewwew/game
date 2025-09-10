import tkinter as tk
from tkinter import ttk, messagebox
import sys
import ast

class GameMain:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 游戏主界面")
        self.root.geometry("1000x700")
        self.root.configure(bg='#2c3e50')
        
        # 角色属性
        self.attributes = {
            '体质': 0,
            '智力': 0,
            '情商': 0,
            '幸运': 0
        }
        
        # 游戏状态
        self.level = 1
        self.experience = 0
        self.health = 100
        self.max_health = 100
        self.magic = 50
        self.max_magic = 50
        
        # 创建界面
        self.create_widgets()
        
        # 如果有命令行参数，加载角色属性
        if len(sys.argv) > 1:
            self.load_character_attributes(sys.argv[1])
    
    def create_widgets(self):
        # 主标题
        title_label = tk.Label(
            self.root,
            text="🎮 游戏主界面",
            font=("Arial", 24, "bold"),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        title_label.pack(pady=20)
        
        # 主框架
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # 左侧 - 角色信息
        left_frame = tk.Frame(main_frame, bg='#34495e', relief='raised', bd=2)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # 角色信息标题
        char_title = tk.Label(
            left_frame,
            text="👤 角色信息",
            font=("Arial", 16, "bold"),
            bg='#34495e',
            fg='#ecf0f1'
        )
        char_title.pack(pady=15)
        
        # 角色属性显示
        self.attr_frame = tk.Frame(left_frame, bg='#34495e')
        self.attr_frame.pack(expand=True, fill='both', padx=20, pady=10)
        
        # 创建属性显示
        self.create_attribute_display()
        
        # 角色状态
        self.create_status_display(left_frame)
        
        # 右侧 - 游戏操作
        right_frame = tk.Frame(main_frame, bg='#34495e', relief='raised', bd=2)
        right_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        # 游戏操作标题
        game_title = tk.Label(
            right_frame,
            text="🎮 游戏操作",
            font=("Arial", 16, "bold"),
            bg='#34495e',
            fg='#ecf0f1'
        )
        game_title.pack(pady=15)
        
        # 游戏按钮区域
        self.create_game_buttons(right_frame)
        
        # 游戏日志区域
        self.create_game_log(right_frame)
    
    def create_attribute_display(self):
        """创建属性显示"""
        for attr_name in self.attributes.keys():
            attr_frame = tk.Frame(self.attr_frame, bg='#34495e')
            attr_frame.pack(fill='x', pady=5)
            
            # 属性名称
            name_label = tk.Label(
                attr_frame,
                text=f"{attr_name}:",
                font=("Arial", 12, "bold"),
                bg='#34495e',
                fg='#ecf0f1',
                width=8,
                anchor='w'
            )
            name_label.pack(side='left')
            
            # 属性值
            value_label = tk.Label(
                attr_frame,
                text="0",
                font=("Arial", 12, "bold"),
                bg='#34495e',
                fg='#e74c3c',
                width=3
            )
            value_label.pack(side='left', padx=10)
            
            # 属性条
            progress_frame = tk.Frame(attr_frame, bg='#34495e')
            progress_frame.pack(side='left', fill='x', expand=True, padx=10)
            
            progress_bar = tk.Canvas(
                progress_frame,
                height=20,
                bg='#2c3e50',
                highlightthickness=0
            )
            progress_bar.pack(fill='x')
            
            # 存储引用
            if not hasattr(self, 'attr_labels'):
                self.attr_labels = {}
            if not hasattr(self, 'progress_bars'):
                self.progress_bars = {}
            
            self.attr_labels[attr_name] = value_label
            self.progress_bars[attr_name] = progress_bar
    
    def create_status_display(self, parent):
        """创建状态显示"""
        status_frame = tk.Frame(parent, bg='#34495e')
        status_frame.pack(fill='x', padx=20, pady=10)
        
        # 等级
        level_frame = tk.Frame(status_frame, bg='#34495e')
        level_frame.pack(fill='x', pady=5)
        
        tk.Label(
            level_frame,
            text="等级:",
            font=("Arial", 12, "bold"),
            bg='#34495e',
            fg='#ecf0f1'
        ).pack(side='left')
        
        self.level_label = tk.Label(
            level_frame,
            text="1",
            font=("Arial", 12, "bold"),
            bg='#34495e',
            fg='#f39c12'
        )
        self.level_label.pack(side='left', padx=10)
        
        # 生命值
        health_frame = tk.Frame(status_frame, bg='#34495e')
        health_frame.pack(fill='x', pady=5)
        
        tk.Label(
            health_frame,
            text="生命值:",
            font=("Arial", 12, "bold"),
            bg='#34495e',
            fg='#ecf0f1'
        ).pack(side='left')
        
        self.health_label = tk.Label(
            health_frame,
            text="100/100",
            font=("Arial", 12, "bold"),
            bg='#34495e',
            fg='#e74c3c'
        )
        self.health_label.pack(side='left', padx=10)
        
        # 魔法值
        magic_frame = tk.Frame(status_frame, bg='#34495e')
        magic_frame.pack(fill='x', pady=5)
        
        tk.Label(
            magic_frame,
            text="魔法值:",
            font=("Arial", 12, "bold"),
            bg='#34495e',
            fg='#ecf0f1'
        ).pack(side='left')
        
        self.magic_label = tk.Label(
            magic_frame,
            text="50/50",
            font=("Arial", 12, "bold"),
            bg='#34495e',
            fg='#3498db'
        )
        self.magic_label.pack(side='left', padx=10)
    
    def create_game_buttons(self, parent):
        """创建游戏按钮"""
        button_frame = tk.Frame(parent, bg='#34495e')
        button_frame.pack(expand=True, fill='both', padx=20, pady=10)
        
        # 战斗按钮
        battle_button = tk.Button(
            button_frame,
            text="⚔️ 战斗",
            font=("Arial", 14, "bold"),
            bg='#e74c3c',
            fg='white',
            relief='raised',
            bd=3,
            command=self.start_battle,
            height=2
        )
        battle_button.pack(fill='x', pady=10)
        
        # 探索按钮
        explore_button = tk.Button(
            button_frame,
            text="🗺️ 探索",
            font=("Arial", 14, "bold"),
            bg='#27ae60',
            fg='white',
            relief='raised',
            bd=3,
            command=self.start_exploration,
            height=2
        )
        explore_button.pack(fill='x', pady=10)
        
        # 商店按钮
        shop_button = tk.Button(
            button_frame,
            text="🏪 商店",
            font=("Arial", 14, "bold"),
            bg='#f39c12',
            fg='white',
            relief='raised',
            bd=3,
            command=self.open_shop,
            height=2
        )
        shop_button.pack(fill='x', pady=10)
        
        # 技能按钮
        skill_button = tk.Button(
            button_frame,
            text="📚 技能",
            font=("Arial", 14, "bold"),
            bg='#9b59b6',
            fg='white',
            relief='raised',
            bd=3,
            command=self.open_skills,
            height=2
        )
        skill_button.pack(fill='x', pady=10)
        
        # 背包按钮
        inventory_button = tk.Button(
            button_frame,
            text="🎒 背包",
            font=("Arial", 14, "bold"),
            bg='#34495e',
            fg='white',
            relief='raised',
            bd=3,
            command=self.open_inventory,
            height=2
        )
        inventory_button.pack(fill='x', pady=10)
    
    def create_game_log(self, parent):
        """创建游戏日志"""
        log_frame = tk.Frame(parent, bg='#34495e')
        log_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(
            log_frame,
            text="📝 游戏日志",
            font=("Arial", 12, "bold"),
            bg='#34495e',
            fg='#ecf0f1'
        ).pack(anchor='w')
        
        # 日志文本框
        self.log_text = tk.Text(
            log_frame,
            height=8,
            width=40,
            font=("Arial", 10),
            bg='#2c3e50',
            fg='#ecf0f1',
            wrap='word',
            state='disabled'
        )
        self.log_text.pack(fill='x', pady=5)
        
        # 滚动条
        scrollbar = tk.Scrollbar(log_frame, orient='vertical', command=self.log_text.yview)
        scrollbar.pack(side='right', fill='y')
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        # 添加欢迎消息
        self.add_log("欢迎来到游戏世界！")
        self.add_log("您的冒险即将开始...")
    
    def load_character_attributes(self, attr_string):
        """加载角色属性"""
        try:
            # 解析属性字符串
            attr_dict = ast.literal_eval(attr_string)
            self.attributes.update(attr_dict)
            self.update_attribute_display()
            self.add_log(f"角色属性已加载：{attr_dict}")
        except Exception as e:
            self.add_log(f"加载角色属性失败：{str(e)}")
    
    def update_attribute_display(self):
        """更新属性显示"""
        for attr_name, value in self.attributes.items():
            if attr_name in self.attr_labels:
                self.attr_labels[attr_name].config(text=str(value))
                # 更新进度条
                self.update_progress_bar(attr_name, value)
    
    def update_progress_bar(self, attr_name, value):
        """更新属性进度条"""
        if attr_name in self.progress_bars:
            canvas = self.progress_bars[attr_name]
            canvas.delete("all")
            
            # 计算进度条长度（最大10）
            max_value = 10
            progress = min(value / max_value, 1.0)
            bar_width = int(progress * 200)  # 进度条最大宽度200
            
            # 绘制进度条
            if bar_width > 0:
                canvas.create_rectangle(0, 0, bar_width, 20, fill='#e74c3c', outline='')
    
    def add_log(self, message):
        """添加日志消息"""
        self.log_text.config(state='normal')
        self.log_text.insert('end', f"{message}\n")
        self.log_text.see('end')
        self.log_text.config(state='disabled')
    
    def start_battle(self):
        """开始战斗"""
        self.add_log("进入战斗！")
        messagebox.showinfo("战斗", "战斗功能开发中...")
    
    def start_exploration(self):
        """开始探索"""
        self.add_log("开始探索...")
        messagebox.showinfo("探索", "探索功能开发中...")
    
    def open_shop(self):
        """打开商店"""
        self.add_log("进入商店")
        messagebox.showinfo("商店", "商店功能开发中...")
    
    def open_skills(self):
        """打开技能界面"""
        self.add_log("查看技能")
        messagebox.showinfo("技能", "技能功能开发中...")
    
    def open_inventory(self):
        """打开背包"""
        self.add_log("查看背包")
        messagebox.showinfo("背包", "背包功能开发中...")

def main():
    root = tk.Tk()
    app = GameMain(root)
    root.mainloop()

if __name__ == "__main__":
    main()
