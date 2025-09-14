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
        
        # 左侧 - 事件和选择区域
        left_frame = tk.Frame(main_frame, bg='#34495e', relief='raised', bd=2)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # 游戏标题
        game_title = tk.Label(
            left_frame,
            text="🎮 游戏事件",
            font=("Arial", 16, "bold"),
            bg='#34495e',
            fg='#ecf0f1'
        )
        game_title.pack(pady=15)
        
        # 事件显示区域
        self.create_event_display(left_frame)
        
        # 选择按钮区域
        self.create_choice_buttons(left_frame)
        
        # 右侧 - 游戏日志区域
        right_frame = tk.Frame(main_frame, bg='#34495e', relief='raised', bd=2)
        right_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        # 游戏日志区域
        self.create_game_log(right_frame)
    
    def create_event_display(self, parent):
        """创建事件显示"""
        self.event_text = tk.Text(
            parent,
            height=15,
            width=50,
            font=("Arial", 12),
            bg='#2c3e50',
            fg='#ecf0f1',
            wrap='word',
            state='disabled'
        )
        self.event_text.pack(padx=20, pady=10)
        
        # 添加初始事件
        self.show_initial_event()
    
    def create_choice_buttons(self, parent):
        """创建选择按钮"""
        self.choice_frame = tk.Frame(parent, bg='#34495e')
        self.choice_frame.pack(fill='x', padx=20, pady=10)
        
        # 添加初始选择按钮
        self.show_initial_choices()
    
    def show_initial_event(self):
        """显示初始事件"""
        self.event_text.config(state='normal')
        self.event_text.delete(1.0, 'end')
        self.event_text.insert('end', "🎮 欢迎来到游戏世界！\n\n")
        self.event_text.insert('end', "你是一名勇敢的冒险者，面前有三条道路：\n\n")
        self.event_text.insert('end', "1. 🗡️ 前往危险的森林探险\n")
        self.event_text.insert('end', "2. 🏰 进入神秘的城堡\n")
        self.event_text.insert('end', "3. 🏪 访问友好的村庄\n\n")
        self.event_text.insert('end', "请选择你的道路...")
        self.event_text.config(state='disabled')
    
    def show_initial_choices(self):
        """显示初始选择按钮"""
        # 清除现有按钮
        for widget in self.choice_frame.winfo_children():
            widget.destroy()
        
        # 森林探险按钮
        forest_button = tk.Button(
            self.choice_frame,
            text="🗡️ 前往森林探险",
            font=("Arial", 12, "bold"),
            bg='#27ae60',
            fg='white',
            relief='raised',
            bd=3,
            command=self.choose_forest,
            height=2
        )
        forest_button.pack(fill='x', pady=5)
        
        # 城堡按钮
        castle_button = tk.Button(
            self.choice_frame,
            text="🏰 进入神秘城堡",
            font=("Arial", 12, "bold"),
            bg='#9b59b6',
            fg='white',
            relief='raised',
            bd=3,
            command=self.choose_castle,
            height=2
        )
        castle_button.pack(fill='x', pady=5)
        
        # 村庄按钮
        village_button = tk.Button(
            self.choice_frame,
            text="🏪 访问友好村庄",
            font=("Arial", 12, "bold"),
            bg='#f39c12',
            fg='white',
            relief='raised',
            bd=3,
            command=self.choose_village,
            height=2
        )
        village_button.pack(fill='x', pady=5)
    
    def choose_forest(self):
        """选择森林探险"""
        self.add_log("选择了森林探险")
        self.show_forest_event()
    
    def choose_castle(self):
        """选择城堡"""
        self.add_log("选择了神秘城堡")
        self.show_castle_event()
    
    def choose_village(self):
        """选择村庄"""
        self.add_log("选择了友好村庄")
        self.show_village_event()
    
    def show_forest_event(self):
        """显示森林事件"""
        self.event_text.config(state='normal')
        self.event_text.delete(1.0, 'end')
        self.event_text.insert('end', "🌲 森林探险\n\n")
        self.event_text.insert('end', "你进入了茂密的森林，阳光透过树叶洒下斑驳的光影。\n\n")
        self.event_text.insert('end', "突然，你听到前方传来奇怪的声音...\n\n")
        self.event_text.insert('end', "1. 🔍 悄悄接近查看\n")
        self.event_text.insert('end', "2. 🏃 快速离开\n")
        self.event_text.insert('end', "3. 🗣️ 大声询问")
        self.event_text.config(state='disabled')
        
        # 更新选择按钮
        self.update_forest_choices()
    
    def show_castle_event(self):
        """显示城堡事件"""
        self.event_text.config(state='normal')
        self.event_text.delete(1.0, 'end')
        self.event_text.insert('end', "🏰 神秘城堡\n\n")
        self.event_text.insert('end', "你站在一座古老的城堡前，石墙上爬满了藤蔓。\n\n")
        self.event_text.insert('end', "城堡的大门半开着，里面传来微弱的光亮...\n\n")
        self.event_text.insert('end', "1. 🚪 推门进入\n")
        self.event_text.insert('end', "2. 🔍 先观察周围\n")
        self.event_text.insert('end', "3. 🏃 离开这里")
        self.event_text.config(state='disabled')
        
        # 更新选择按钮
        self.update_castle_choices()
    
    def show_village_event(self):
        """显示村庄事件"""
        self.event_text.config(state='normal')
        self.event_text.delete(1.0, 'end')
        self.event_text.insert('end', "🏪 友好村庄\n\n")
        self.event_text.insert('end', "你来到了一个宁静的村庄，村民们正在忙碌着。\n\n")
        self.event_text.insert('end', "一位老人向你招手，似乎有话要说...\n\n")
        self.event_text.insert('end', "1. 👋 上前打招呼\n")
        self.event_text.insert('end', "2. 🏪 先去商店看看\n")
        self.event_text.insert('end', "3. 🏃 继续赶路")
        self.event_text.config(state='disabled')
        
        # 更新选择按钮
        self.update_village_choices()
    
    def update_forest_choices(self):
        """更新森林选择按钮"""
        for widget in self.choice_frame.winfo_children():
            widget.destroy()
        
        choice1 = tk.Button(
            self.choice_frame,
            text="🔍 悄悄接近查看",
            font=("Arial", 12, "bold"),
            bg='#3498db',
            fg='white',
            relief='raised',
            bd=3,
            command=lambda: self.add_log("悄悄接近查看"),
            height=2
        )
        choice1.pack(fill='x', pady=5)
        
        choice2 = tk.Button(
            self.choice_frame,
            text="🏃 快速离开",
            font=("Arial", 12, "bold"),
            bg='#e74c3c',
            fg='white',
            relief='raised',
            bd=3,
            command=lambda: self.add_log("快速离开"),
            height=2
        )
        choice2.pack(fill='x', pady=5)
        
        choice3 = tk.Button(
            self.choice_frame,
            text="🗣️ 大声询问",
            font=("Arial", 12, "bold"),
            bg='#f39c12',
            fg='white',
            relief='raised',
            bd=3,
            command=lambda: self.add_log("大声询问"),
            height=2
        )
        choice3.pack(fill='x', pady=5)
    
    def update_castle_choices(self):
        """更新城堡选择按钮"""
        for widget in self.choice_frame.winfo_children():
            widget.destroy()
        
        choice1 = tk.Button(
            self.choice_frame,
            text="🚪 推门进入",
            font=("Arial", 12, "bold"),
            bg='#9b59b6',
            fg='white',
            relief='raised',
            bd=3,
            command=lambda: self.add_log("推门进入城堡"),
            height=2
        )
        choice1.pack(fill='x', pady=5)
        
        choice2 = tk.Button(
            self.choice_frame,
            text="🔍 先观察周围",
            font=("Arial", 12, "bold"),
            bg='#3498db',
            fg='white',
            relief='raised',
            bd=3,
            command=lambda: self.add_log("观察周围环境"),
            height=2
        )
        choice2.pack(fill='x', pady=5)
        
        choice3 = tk.Button(
            self.choice_frame,
            text="🏃 离开这里",
            font=("Arial", 12, "bold"),
            bg='#e74c3c',
            fg='white',
            relief='raised',
            bd=3,
            command=lambda: self.add_log("离开城堡"),
            height=2
        )
        choice3.pack(fill='x', pady=5)
    
    def update_village_choices(self):
        """更新村庄选择按钮"""
        for widget in self.choice_frame.winfo_children():
            widget.destroy()
        
        choice1 = tk.Button(
            self.choice_frame,
            text="👋 上前打招呼",
            font=("Arial", 12, "bold"),
            bg='#27ae60',
            fg='white',
            relief='raised',
            bd=3,
            command=lambda: self.add_log("向老人打招呼"),
            height=2
        )
        choice1.pack(fill='x', pady=5)
        
        choice2 = tk.Button(
            self.choice_frame,
            text="🏪 先去商店看看",
            font=("Arial", 12, "bold"),
            bg='#f39c12',
            fg='white',
            relief='raised',
            bd=3,
            command=lambda: self.add_log("前往商店"),
            height=2
        )
        choice2.pack(fill='x', pady=5)
        
        choice3 = tk.Button(
            self.choice_frame,
            text="🏃 继续赶路",
            font=("Arial", 12, "bold"),
            bg='#95a5a6',
            fg='white',
            relief='raised',
            bd=3,
            command=lambda: self.add_log("继续赶路"),
            height=2
        )
        choice3.pack(fill='x', pady=5)
    
    
    
    def create_game_log(self, parent):
        """创建游戏日志"""
        # 日志标题
        log_title = tk.Label(
            parent,
            text="📝 游戏日志",
            font=("Arial", 16, "bold"),
            bg='#34495e',
            fg='#ecf0f1'
        )
        log_title.pack(pady=15)
        
        # 日志文本框
        self.log_text = tk.Text(
            parent,
            height=25,
            width=40,
            font=("Arial", 10),
            bg='#2c3e50',
            fg='#ecf0f1',
            wrap='word',
            state='disabled'
        )
        self.log_text.pack(padx=20, pady=10)
        
        # 滚动条
        scrollbar = tk.Scrollbar(parent, orient='vertical', command=self.log_text.yview)
        scrollbar.pack(side='right', fill='y', padx=(0, 20), pady=10)
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
            self.add_log(f"角色属性已加载：{attr_dict}")
        except Exception as e:
            self.add_log(f"加载角色属性失败：{str(e)}")
    
    
    def add_log(self, message):
        """添加日志消息"""
        self.log_text.config(state='normal')
        self.log_text.insert('end', f"{message}\n")
        self.log_text.see('end')
        self.log_text.config(state='disabled')
    

def main():
    root = tk.Tk()
    app = GameMain(root)
    root.mainloop()

if __name__ == "__main__":
    main()
