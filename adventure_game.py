import tkinter as tk
from tkinter import ttk, messagebox
import random
import sys
import ast

class AdventureGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 跑团冒险游戏")
        self.root.geometry("1000x700")
        self.root.configure(bg='#2c3e50')
        
        # 游戏状态
        self.day = 1
        self.money = 100  # 初始资金
        self.target_money = 2000  # 目标资金
        self.max_days = 10  # 最大天数
        
        # 角色属性（从start.py传入）
        self.attributes = {
            '体质': 0,
            '智力': 0,
            '情商': 0,
            '幸运': 0
        }
        
        # 背包物品
        self.inventory = {}
        
        # 商品价格（基础价格，会根据幸运值波动）
        self.item_prices = {
            '面包': 10,
            '苹果': 15,
            'CD': 25,
            '器材': 50,
            '宝石': 100,
            '古董': 200,
            '股票': 300,
            '房产': 500
        }
        
        # 每日事件
        self.daily_events = [
            {
                'name': '自由市场',
                'description': '你来到了自由市场，请选择你要购买的货物：',
                'items': ['面包', '苹果', 'CD', '器材']
            },
            {
                'name': '古董店',
                'description': '你发现了一家古董店，店主正在出售一些珍品：',
                'items': ['古董', '宝石', 'CD', '器材']
            },
            {
                'name': '投资中心',
                'description': '你来到了投资中心，可以投资一些金融产品：',
                'items': ['股票', '房产', '宝石', '古董']
            },
            {
                'name': '黑市',
                'description': '你偶然发现了黑市，这里有一些特殊商品：',
                'items': ['器材', '宝石', '古董', '股票']
            }
        ]
        
        # 特殊事件
        self.special_events = [
            {
                'name': '幸运发现',
                'description': '你在路上发现了一个钱包！',
                'money_bonus': 50,
                'condition': '幸运'
            },
            {
                'name': '智慧投资',
                'description': '你的智慧让你发现了一个投资机会！',
                'money_bonus': 100,
                'condition': '智力'
            },
            {
                'name': '社交机会',
                'description': '你通过社交获得了一个赚钱的机会！',
                'money_bonus': 75,
                'condition': '情商'
            },
            {
                'name': '体力工作',
                'description': '你通过体力劳动赚取了一些外快！',
                'money_bonus': 30,
                'condition': '体质'
            }
        ]
        
        # 创建界面
        self.create_widgets()
        
        # 如果有命令行参数，加载角色属性
        if len(sys.argv) > 1:
            self.load_character_attributes(sys.argv[1])
        
        # 开始第一天
        self.start_new_day()
    
    def create_widgets(self):
        # 主标题
        title_label = tk.Label(
            self.root,
            text="🎮 跑团冒险游戏",
            font=("Arial", 24, "bold"),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        title_label.pack(pady=20)
        
        # 主框架
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # 左侧 - 游戏状态
        left_frame = tk.Frame(main_frame, bg='#34495e', relief='raised', bd=2)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # 游戏状态标题
        status_title = tk.Label(
            left_frame,
            text="📊 游戏状态",
            font=("Arial", 16, "bold"),
            bg='#34495e',
            fg='#ecf0f1'
        )
        status_title.pack(pady=15)
        
        # 状态显示
        self.create_status_display(left_frame)
        
        # 角色属性显示
        self.create_attribute_display(left_frame)
        
        # 背包显示
        self.create_inventory_display(left_frame)
        
        # 右侧 - 游戏内容
        right_frame = tk.Frame(main_frame, bg='#34495e', relief='raised', bd=2)
        right_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        # 游戏内容标题
        content_title = tk.Label(
            right_frame,
            text="🎯 游戏内容",
            font=("Arial", 16, "bold"),
            bg='#34495e',
            fg='#ecf0f1'
        )
        content_title.pack(pady=15)
        
        # 事件描述区域
        self.create_event_display(right_frame)
        
        # 选择按钮区域
        self.create_choice_buttons(right_frame)
        
        # 游戏日志
        self.create_game_log(right_frame)
    
    def create_status_display(self, parent):
        """创建状态显示"""
        status_frame = tk.Frame(parent, bg='#34495e')
        status_frame.pack(fill='x', padx=20, pady=10)
        
        # 天数
        day_frame = tk.Frame(status_frame, bg='#34495e')
        day_frame.pack(fill='x', pady=5)
        
        tk.Label(
            day_frame,
            text="第几天:",
            font=("Arial", 12, "bold"),
            bg='#34495e',
            fg='#ecf0f1'
        ).pack(side='left')
        
        self.day_label = tk.Label(
            day_frame,
            text="1",
            font=("Arial", 12, "bold"),
            bg='#34495e',
            fg='#f39c12'
        )
        self.day_label.pack(side='left', padx=10)
        
        # 金钱
        money_frame = tk.Frame(status_frame, bg='#34495e')
        money_frame.pack(fill='x', pady=5)
        
        tk.Label(
            money_frame,
            text="金钱:",
            font=("Arial", 12, "bold"),
            bg='#34495e',
            fg='#ecf0f1'
        ).pack(side='left')
        
        self.money_label = tk.Label(
            money_frame,
            text="100",
            font=("Arial", 12, "bold"),
            bg='#34495e',
            fg='#27ae60'
        )
        self.money_label.pack(side='left', padx=10)
        
        # 目标
        target_frame = tk.Frame(status_frame, bg='#34495e')
        target_frame.pack(fill='x', pady=5)
        
        tk.Label(
            target_frame,
            text="目标:",
            font=("Arial", 12, "bold"),
            bg='#34495e',
            fg='#ecf0f1'
        ).pack(side='left')
        
        self.target_label = tk.Label(
            target_frame,
            text="2000",
            font=("Arial", 12, "bold"),
            bg='#34495e',
            fg='#e74c3c'
        )
        self.target_label.pack(side='left', padx=10)
    
    def create_attribute_display(self, parent):
        """创建属性显示"""
        attr_title = tk.Label(
            parent,
            text="👤 角色属性",
            font=("Arial", 14, "bold"),
            bg='#34495e',
            fg='#ecf0f1'
        )
        attr_title.pack(pady=(20, 10))
        
        self.attr_frame = tk.Frame(parent, bg='#34495e')
        self.attr_frame.pack(fill='x', padx=20, pady=10)
        
        self.attr_labels = {}
        for attr_name in self.attributes.keys():
            attr_frame = tk.Frame(self.attr_frame, bg='#34495e')
            attr_frame.pack(fill='x', pady=2)
            
            name_label = tk.Label(
                attr_frame,
                text=f"{attr_name}:",
                font=("Arial", 10, "bold"),
                bg='#34495e',
                fg='#ecf0f1',
                width=6,
                anchor='w'
            )
            name_label.pack(side='left')
            
            value_label = tk.Label(
                attr_frame,
                text="0",
                font=("Arial", 10, "bold"),
                bg='#34495e',
                fg='#e74c3c',
                width=3
            )
            value_label.pack(side='left', padx=5)
            
            self.attr_labels[attr_name] = value_label
    
    def create_inventory_display(self, parent):
        """创建背包显示"""
        inv_title = tk.Label(
            parent,
            text="🎒 背包",
            font=("Arial", 14, "bold"),
            bg='#34495e',
            fg='#ecf0f1'
        )
        inv_title.pack(pady=(20, 10))
        
        self.inv_text = tk.Text(
            parent,
            height=6,
            width=25,
            font=("Arial", 9),
            bg='#2c3e50',
            fg='#ecf0f1',
            wrap='word',
            state='disabled'
        )
        self.inv_text.pack(padx=20, pady=10)
    
    def create_event_display(self, parent):
        """创建事件显示"""
        self.event_text = tk.Text(
            parent,
            height=8,
            width=50,
            font=("Arial", 12),
            bg='#2c3e50',
            fg='#ecf0f1',
            wrap='word',
            state='disabled'
        )
        self.event_text.pack(padx=20, pady=10)
    
    def create_choice_buttons(self, parent):
        """创建选择按钮"""
        self.choice_frame = tk.Frame(parent, bg='#34495e')
        self.choice_frame.pack(fill='x', padx=20, pady=10)
    
    def create_game_log(self, parent):
        """创建游戏日志"""
        log_title = tk.Label(
            parent,
            text="📝 游戏日志",
            font=("Arial", 12, "bold"),
            bg='#34495e',
            fg='#ecf0f1'
        )
        log_title.pack(pady=(20, 5))
        
        self.log_text = tk.Text(
            parent,
            height=6,
            width=50,
            font=("Arial", 9),
            bg='#2c3e50',
            fg='#ecf0f1',
            wrap='word',
            state='disabled'
        )
        self.log_text.pack(padx=20, pady=10)
    
    def load_character_attributes(self, attr_string):
        """加载角色属性"""
        try:
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
    
    def update_status_display(self):
        """更新状态显示"""
        self.day_label.config(text=str(self.day))
        self.money_label.config(text=str(self.money))
        self.target_label.config(text=str(self.target_money))
    
    def update_inventory_display(self):
        """更新背包显示"""
        self.inv_text.config(state='normal')
        self.inv_text.delete(1.0, 'end')
        
        if not self.inventory:
            self.inv_text.insert('end', "背包为空")
        else:
            for item, count in self.inventory.items():
                self.inv_text.insert('end', f"{item}: {count}个\n")
        
        self.inv_text.config(state='disabled')
    
    def add_log(self, message):
        """添加日志消息"""
        self.log_text.config(state='normal')
        self.log_text.insert('end', f"第{self.day}天: {message}\n")
        self.log_text.see('end')
        self.log_text.config(state='disabled')
    
    def start_new_day(self):
        """开始新的一天"""
        self.update_status_display()
        self.update_inventory_display()
        
        # 随机选择事件
        event = random.choice(self.daily_events)
        
        # 显示事件
        self.event_text.config(state='normal')
        self.event_text.delete(1.0, 'end')
        self.event_text.insert('end', f"第{self.day}天：\n\n")
        self.event_text.insert('end', f"{event['description']}\n\n")
        
        # 计算商品价格（根据幸运值调整）
        luck_bonus = self.attributes.get('幸运', 0) * 0.1  # 幸运值影响价格
        for i, item in enumerate(event['items']):
            base_price = self.item_prices[item]
            adjusted_price = int(base_price * (1 - luck_bonus))
            self.event_text.insert('end', f"{i+1}. {item} - {adjusted_price}金币\n")
        
        self.event_text.config(state='disabled')
        
        # 创建选择按钮
        self.create_choice_buttons_for_event(event)
        
        self.add_log(f"来到了{event['name']}")
    
    def create_choice_buttons_for_event(self, event):
        """为事件创建选择按钮"""
        # 清除现有按钮
        for widget in self.choice_frame.winfo_children():
            widget.destroy()
        
        # 计算商品价格
        luck_bonus = self.attributes.get('幸运', 0) * 0.1
        for i, item in enumerate(event['items']):
            base_price = self.item_prices[item]
            adjusted_price = int(base_price * (1 - luck_bonus))
            
            button = tk.Button(
                self.choice_frame,
                text=f"{item} - {adjusted_price}金币",
                font=("Arial", 10, "bold"),
                bg='#3498db',
                fg='white',
                relief='raised',
                bd=2,
                command=lambda item=item, price=adjusted_price: self.make_choice(item, price),
                height=2
            )
            button.pack(fill='x', pady=5)
    
    def make_choice(self, item, price):
        """做出选择"""
        if self.money < price:
            self.add_log(f"金钱不足，无法购买{item}")
            messagebox.showwarning("金钱不足", f"你需要{price}金币，但只有{self.money}金币！")
            return
        
        # 购买物品
        self.money -= price
        if item in self.inventory:
            self.inventory[item] += 1
        else:
            self.inventory[item] = 1
        
        self.add_log(f"购买了{item}，花费{price}金币")
        
        # 检查特殊事件
        self.check_special_events()
        
        # 更新显示
        self.update_status_display()
        self.update_inventory_display()
        
        # 检查胜利条件
        if self.money >= self.target_money:
            self.game_win()
            return
        
        # 进入下一天
        self.next_day()
    
    def check_special_events(self):
        """检查特殊事件"""
        # 根据属性值决定是否触发特殊事件
        for event in self.special_events:
            attr_value = self.attributes.get(event['condition'], 0)
            if attr_value > 0 and random.random() < (attr_value / 10):  # 属性值越高，触发概率越大
                self.money += event['money_bonus']
                self.add_log(f"触发特殊事件：{event['name']}！获得{event['money_bonus']}金币")
                break
    
    def next_day(self):
        """进入下一天"""
        self.day += 1
        
        if self.day > self.max_days:
            self.game_over()
            return
        
        # 随机获得一些金钱（模拟其他收入）
        daily_income = random.randint(10, 50)
        self.money += daily_income
        self.add_log(f"获得日常收入{daily_income}金币")
        
        # 开始新的一天
        self.start_new_day()
    
    def game_win(self):
        """游戏胜利"""
        self.event_text.config(state='normal')
        self.event_text.delete(1.0, 'end')
        self.event_text.insert('end', f"🎉 恭喜！你成功了！\n\n")
        self.event_text.insert('end', f"你在第{self.day}天就攒够了{self.target_money}金币！\n\n")
        self.event_text.insert('end', f"最终金钱：{self.money}金币\n")
        self.event_text.insert('end', f"剩余天数：{self.max_days - self.day + 1}天\n\n")
        self.event_text.insert('end', "你是一个成功的商人！")
        self.event_text.config(state='disabled')
        
        # 清除选择按钮
        for widget in self.choice_frame.winfo_children():
            widget.destroy()
        
        # 添加重新开始按钮
        restart_button = tk.Button(
            self.choice_frame,
            text="🔄 重新开始",
            font=("Arial", 12, "bold"),
            bg='#27ae60',
            fg='white',
            relief='raised',
            bd=3,
            command=self.restart_game,
            height=2
        )
        restart_button.pack(fill='x', pady=10)
        
        self.add_log("游戏胜利！")
        messagebox.showinfo("游戏胜利", f"恭喜！你在第{self.day}天就攒够了{self.target_money}金币！")
    
    def game_over(self):
        """游戏结束"""
        self.event_text.config(state='normal')
        self.event_text.delete(1.0, 'end')
        self.event_text.insert('end', f"😞 游戏结束\n\n")
        self.event_text.insert('end', f"10天过去了，你只攒到了{self.money}金币\n\n")
        self.event_text.insert('end', f"目标：{self.target_money}金币\n")
        self.event_text.insert('end', f"差距：{self.target_money - self.money}金币\n\n")
        self.event_text.insert('end', "不要灰心，再来一次吧！")
        self.event_text.config(state='disabled')
        
        # 清除选择按钮
        for widget in self.choice_frame.winfo_children():
            widget.destroy()
        
        # 添加重新开始按钮
        restart_button = tk.Button(
            self.choice_frame,
            text="🔄 重新开始",
            font=("Arial", 12, "bold"),
            bg='#e74c3c',
            fg='white',
            relief='raised',
            bd=3,
            command=self.restart_game,
            height=2
        )
        restart_button.pack(fill='x', pady=10)
        
        self.add_log("游戏结束")
        messagebox.showinfo("游戏结束", f"10天过去了，你只攒到了{self.money}金币，距离目标还差{self.target_money - self.money}金币。")
    
    def restart_game(self):
        """重新开始游戏"""
        self.day = 1
        self.money = 100
        self.inventory = {}
        self.start_new_day()

def main():
    root = tk.Tk()
    app = AdventureGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
