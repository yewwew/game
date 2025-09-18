import random
import time
import tkinter as tk
from tkinter import ttk, messagebox
import threading

class DiceGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎲 角色属性生成器")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # 属性数据
        self.attributes = {
            '体质': 0,
            '智力': 0,
            '情商': 0,
            '幸运': 0
        }
        self.roll_history = []
        
        # 创建界面
        self.create_widgets()
        
    def create_widgets(self):
        # 标题
        title_label = tk.Label(
            self.root, 
            text="🎮 角色属性生成器", 
            font=("Arial", 24, "bold"),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        title_label.pack(pady=20)
        
        # 说明文字
        desc_label = tk.Label(
            self.root,
            text="掷骰子确定角色的基础属性（3个6面骰子，去掉最低值）",
            font=("Arial", 12),
            bg='#f0f0f0',
            fg='#7f8c8d'
        )
        desc_label.pack(pady=10)
        
        # 主框架
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # 左侧 - 属性显示区域
        left_frame = tk.Frame(main_frame, bg='#ecf0f1', relief='raised', bd=2)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # 属性标题
        attr_title = tk.Label(
            left_frame,
            text="📊 角色属性",
            font=("Arial", 16, "bold"),
            bg='#ecf0f1',
            fg='#2c3e50'
        )
        attr_title.pack(pady=15)
        
        # 属性显示区域
        self.attr_frame = tk.Frame(left_frame, bg='#ecf0f1')
        self.attr_frame.pack(expand=True, fill='both', padx=20, pady=10)
        
        # 创建属性显示标签
        self.attr_labels = {}
        for attr_name in self.attributes.keys():
            self.create_attribute_display(attr_name)
        
        # 总点数显示
        self.total_label = tk.Label(
            left_frame,
            text="总点数: 0",
            font=("Arial", 14, "bold"),
            bg='#ecf0f1',
            fg='#e74c3c'
        )
        self.total_label.pack(pady=10)
        
        # 右侧 - 控制区域
        right_frame = tk.Frame(main_frame, bg='#ecf0f1', relief='raised', bd=2)
        right_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        # 控制标题
        control_title = tk.Label(
            right_frame,
            text="🎮 游戏控制",
            font=("Arial", 16, "bold"),
            bg='#ecf0f1',
            fg='#2c3e50'
        )
        control_title.pack(pady=15)
        
        # 按钮区域
        button_frame = tk.Frame(right_frame, bg='#ecf0f1')
        button_frame.pack(expand=True, fill='both', padx=20, pady=10)
        
        # 掷骰子按钮
        self.roll_button = tk.Button(
            button_frame,
            text="🎲 掷骰子确定所有属性",
            font=("Arial", 12, "bold"),
            bg='#3498db',
            fg='white',
            relief='raised',
            bd=3,
            command=self.roll_all_attributes,
            height=2
        )
        self.roll_button.pack(fill='x', pady=10)
        
        # 进入游戏按钮（初始隐藏）
        self.enter_game_button = tk.Button(
            button_frame,
            text="🚀 进入游戏",
            font=("Arial", 12, "bold"),
            bg='#27ae60',
            fg='white',
            relief='raised',
            bd=3,
            command=self.enter_game,
            height=2
        )
        # 初始状态隐藏
        self.enter_game_button.pack_forget()
        
        # 游戏状态标记
        self.game_ready = False
        
        # 骰子动画区域
        self.dice_frame = tk.Frame(right_frame, bg='#ecf0f1')
        self.dice_frame.pack(fill='x', padx=20, pady=10)
        
        self.dice_labels = []
        for i in range(2):  # 改为2个骰子
            dice_label = tk.Label(
                self.dice_frame,
                text="⚀",
                font=("Arial", 30),
                bg='#ecf0f1',
                fg='#2c3e50'
            )
            dice_label.pack(side='left', padx=5)
            self.dice_labels.append(dice_label)
        
        # 初始化属性显示
        self.update_attribute_display()
    
    def create_attribute_display(self, attr_name):
        """创建单个属性显示"""
        attr_frame = tk.Frame(self.attr_frame, bg='#ecf0f1')
        attr_frame.pack(fill='x', pady=5)
        
        # 属性名称
        name_label = tk.Label(
            attr_frame,
            text=f"{attr_name}:",
            font=("Arial", 14, "bold"),
            bg='#ecf0f1',
            fg='#2c3e50',
            width=8,
            anchor='w'
        )
        name_label.pack(side='left')
        
        # 属性值
        value_label = tk.Label(
            attr_frame,
            text="0",
            font=("Arial", 14, "bold"),
            bg='#ecf0f1',
            fg='#e74c3c',
            width=3
        )
        value_label.pack(side='left', padx=10)
        
        # 骰子结果显示
        dice_label = tk.Label(
            attr_frame,
            text="",
            font=("Arial", 12),
            bg='#ecf0f1',
            fg='#7f8c8d'
        )
        dice_label.pack(side='left')
        
        self.attr_labels[attr_name] = {
            'value': value_label,
            'dice': dice_label
        }
    
    def update_attribute_display(self):
        """更新属性显示"""
        total = 0
        for attr_name, value in self.attributes.items():
            self.attr_labels[attr_name]['value'].config(text=str(value))
            total += value
        
        self.total_label.config(text=f"总点数: {total}")
    
    def roll_dice(self, sides=5, count=2):
        """掷骰子"""
        return [random.randint(0, sides) for _ in range(count)]
    
    def calculate_attribute(self, rolls):
        """计算属性值"""
        # 对于2个骰子，直接相加
        return sum(rolls)
    
    def animate_dice(self, rolls, callback):
        """骰子动画"""
        def animate():
            for _ in range(2):  # 动画次数
                for i, dice_label in enumerate(self.dice_labels):
                    random_face = random.randint(0, 5)
                    dice_label.config(text=self.get_dice_face(random_face))
                self.root.update()
                time.sleep(0.1)
            
            # 显示最终结果
            for i, dice_label in enumerate(self.dice_labels):
                dice_label.config(text=self.get_dice_face(rolls[i]))
            
            callback()
        
        threading.Thread(target=animate, daemon=True).start()
    
    def get_dice_face(self, number):
        """获取骰子面"""
        faces = {
            0: "⚀", 1: "⚁", 2: "⚂", 
            3: "⚃", 4: "⚄", 5: "⚅"
        }
        return faces.get(number, "⚀")
    
    def roll_all_attributes(self):
        """掷所有属性"""
        #self.roll_button.config(state='disabled')
        

        
        def roll_attributes():
            for attr_name in self.attributes.keys():
                rolls = self.roll_dice(5, 2)
                attribute_value = self.calculate_attribute(rolls)
                
                self.attributes[attr_name] = attribute_value
                self.roll_history.append({
                    'attribute': attr_name,
                    'rolls': rolls,
                    'value': attribute_value
                })
                
                # 更新骰子显示
                self.root.after(0, lambda r=rolls: self.animate_dice(r, lambda: None))
                
                # 更新属性显示
                self.root.after(0, self.update_attribute_display)
                
                #time.sleep(1)  # 每个属性之间的延迟
            
            # 掷骰子完成后显示"进入游戏"按钮
            self.root.after(0, self.show_enter_game_button)
        
        threading.Thread(target=roll_attributes, daemon=True).start()
    
    def show_enter_game_button(self):
        """显示进入游戏按钮"""
        if not self.game_ready:
            self.enter_game_button.pack(fill='x', pady=10)
            self.game_ready = True
            # 显示完成提示
            #messagebox.showinfo("属性生成完成", "角色属性已生成完成！\n点击'进入游戏'开始您的冒险！")
    
    def enter_game(self):
        """进入游戏"""
        # 直接启动游戏，不显示中间界面
        self.launch_game()
    
    
    def launch_game(self):
        """启动游戏主程序"""
        try:
            import subprocess
            import sys
            import os
            
            # 获取当前目录
            current_dir = os.path.dirname(os.path.abspath(__file__))
            game_path = os.path.join(current_dir, "game.py")
            
            # 传递角色属性数据
            attr_data = {
                '体质': self.attributes['体质'],
                '智力': self.attributes['智力'],
                '情商': self.attributes['情商'],
                '幸运': self.attributes['幸运']
            }
            
            # 将属性数据转换为JSON字符串以确保正确传递
            import json
            attr_json = json.dumps(attr_data, ensure_ascii=False)
            
            # 启动游戏
            subprocess.Popen([sys.executable, game_path, attr_json])
            
            # 延迟一点时间确保game.py启动，然后关闭start.py
            self.root.after(500, self.close_start)
            
        except Exception as e:
            messagebox.showerror("错误", f"启动游戏失败：{str(e)}")
    
    def close_start(self):
        """关闭start.py界面"""
        self.root.quit()
        self.root.destroy()
    
    def show_detailed_attributes(self):
        """显示详细属性"""
        detailed_window = tk.Toplevel(self.root)
        detailed_window.title("📊 详细属性")
        detailed_window.geometry("400x300")
        detailed_window.configure(bg='#ecf0f1')
        
        tk.Label(
            detailed_window,
            text="📊 角色详细属性",
            font=("Arial", 16, "bold"),
            bg='#ecf0f1',
            fg='#2c3e50'
        ).pack(pady=20)
        
        # 属性详细显示
        for attr_name, value in self.attributes.items():
            attr_frame = tk.Frame(detailed_window, bg='#ecf0f1')
            attr_frame.pack(fill='x', padx=20, pady=5)
            
            tk.Label(
                attr_frame,
                text=f"{attr_name}:",
                font=("Arial", 12, "bold"),
                bg='#ecf0f1',
                fg='#2c3e50',
                width=8,
                anchor='w'
            ).pack(side='left')
            
            tk.Label(
                attr_frame,
                text=f"{value} 点",
                font=("Arial", 12),
                bg='#ecf0f1',
                fg='#e74c3c'
            ).pack(side='left', padx=10)
    
    def show_reroll_menu(self):
        """显示重新掷骰菜单"""
        if not self.attributes or all(v == 0 for v in self.attributes.values()):
            messagebox.showwarning("警告", "请先掷骰子生成属性！")
            return
    
    def reroll_attribute(self, attribute_name, window):
        """重新掷某个属性"""
        window.destroy()
        

        
        def roll():
            rolls = self.roll_dice(5, 2)
            new_value = self.calculate_attribute(rolls)
            old_value = self.attributes[attribute_name]
            
            self.attributes[attribute_name] = new_value
            
            # 更新历史记录
           
            

        
        threading.Thread(target=roll, daemon=True).start()
    
    

def main():
    root = tk.Tk()
    app = DiceGameGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()