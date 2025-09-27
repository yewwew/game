# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import ast
import random
import json
import os

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
        self.choice_count = 0  # 选择计数器
        
        # 当前事件
        self.current_event = None
        self.current_choices = []
        
        # 初始化事件库
        self.init_event_library()
        
        # 创建界面
        self.create_widgets()
        
        # 如果有命令行参数，加载角色属性
        if len(sys.argv) > 1:
            self.load_character_attributes(sys.argv[1])
    
    def init_event_library(self):
        """从JSON文件初始化事件库"""
        try:
            # 获取当前脚本所在目录
            script_dir = os.path.dirname(os.path.abspath(__file__))
            events_file = os.path.join(script_dir, 'events.json')
            
            # 读取JSON文件
            with open(events_file, 'r', encoding='utf-8') as f:
                self.event_library = json.load(f)
            
            # 将JSON中的列表格式转换为元组格式（为了兼容现有代码）
            for event_name, event_data in self.event_library.items():
                for choice in event_data['choices']:
                    for effect_name, effect_value in choice['effects'].items():
                        if isinstance(effect_value, list) and len(effect_value) == 2:
                            choice['effects'][effect_name] = tuple(effect_value)
            
            print("事件库加载成功！")
            
        except FileNotFoundError:
            print("错误：找不到 events.json 文件！")
            # 如果文件不存在，使用默认事件库
            self.event_library = self.get_default_events()
        except json.JSONDecodeError as e:
            print(f"错误：JSON文件格式错误 - {str(e)}")
            self.event_library = self.get_default_events()
        except Exception as e:
            print(f"错误：加载事件库失败 - {str(e)}")
            self.event_library = self.get_default_events()
    
    def get_default_events(self):
        """获取默认事件库（作为备用）"""
        return {
            "默认事件": {
                "description": "🎮 这是一个默认事件，请检查 events.json 文件。",
                "choices": [
                    {"text": "🔧 修复问题", "effects": {"智力": (1, 2)}, "description": "你尝试修复了问题"},
                    {"text": "🏃 离开这里", "effects": {"幸运": (1, 1)}, "description": "你离开了这里"},
                    {"text": "🗣️ 寻求帮助", "effects": {"情商": (1, 1)}, "description": "你寻求了帮助"},
                    {"text": "⏰ 等待", "effects": {"体质": (1, 1)}, "description": "你耐心等待"}
                ]
            }
        }
    
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
        
        # 右侧 - 属性显示和游戏日志区域
        right_frame = tk.Frame(main_frame, bg='#34495e', relief='raised', bd=2)
        right_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        # 属性显示区域
        self.create_attributes_display(right_frame)
        
        # 游戏日志区域
        self.create_game_log(right_frame)
        
        # 所有组件创建完成后，显示初始事件
        self.show_random_event()
    
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
        
        # 初始事件将在所有组件创建后显示
    
    def create_choice_buttons(self, parent):
        """创建选择按钮"""
        self.choice_frame = tk.Frame(parent, bg='#34495e')
        self.choice_frame.pack(fill='x', padx=20, pady=10)
    
    def show_random_event(self):
        """显示随机事件"""
        # 随机选择一个事件
        event_name = random.choice(list(self.event_library.keys()))
        self.current_event = self.event_library[event_name]
        self.current_choices = self.current_event["choices"]
        
        # 显示事件描述
        self.event_text.config(state='normal')
        self.event_text.delete(1.0, 'end')
        self.event_text.insert('end', f"🎮 {event_name}\n\n")
        self.event_text.insert('end', f"{self.current_event['description']}\n\n")
        self.event_text.insert('end', "请选择你的行动...")
        self.event_text.config(state='disabled')
        
        # 更新选择按钮
        self.update_dynamic_choices()
    
    def show_dynamic_choices(self):
        """显示动态选择按钮"""
        self.update_dynamic_choices()
    
    def update_dynamic_choices(self):
        """更新动态选择按钮"""
        # 清除现有按钮
        for widget in self.choice_frame.winfo_children():
            widget.destroy()
        
        if not self.current_choices:
            return
        
        # 创建4个选择按钮
        colors = ['#3498db', '#e74c3c', '#f39c12', '#27ae60']
        
        for i, choice in enumerate(self.current_choices):
            button = tk.Button(
                self.choice_frame,
                text=choice["text"],
                font=("Arial", 12, "bold"),
                bg=colors[i % len(colors)],
                fg='white',
                relief='raised',
                bd=3,
                command=lambda c=choice: self.make_choice(c),
                height=2
            )
            button.pack(fill='x', pady=5)
    
    def make_choice(self, choice):
        """处理选择"""
        # 记录选择
        self.add_log(f"选择了：{choice['text']}")
        
        # 增加选择计数
        self.choice_count += 1
        
        # 应用效果
        self.apply_effects(choice["effects"])
        
        # 显示结果界面
        self.show_choice_result(choice)
    
    def apply_effects(self, effects):
        """应用选择效果"""
        for effect, value in effects.items():
            if effect in self.attributes:
                # 属性效果
                if isinstance(value, tuple):
                    change = random.randint(value[0], value[1])
                else:
                    change = value
                self.attributes[effect] += change
                self.add_log(f"{effect} +{change} (当前: {self.attributes[effect]})")
            elif effect == "health":
                # 生命值效果
                if isinstance(value, tuple):
                    change = random.randint(value[0], value[1])
                else:
                    change = value
                self.health = min(self.max_health, self.health + change)
                self.add_log(f"生命值 +{change} (当前: {self.health})")
            elif effect == "magic":
                # 魔法值效果
                if isinstance(value, tuple):
                    change = random.randint(value[0], value[1])
                else:
                    change = value
                self.magic = min(self.max_magic, self.magic + change)
                self.add_log(f"魔法值 +{change} (当前: {self.magic})")
            elif effect == "experience":
                # 经验值效果
                if isinstance(value, tuple):
                    change = random.randint(value[0], value[1])
                else:
                    change = value
                self.experience += change
                self.add_log(f"经验值 +{change} (当前: {self.experience})")
        
        # 更新属性显示
        self.update_attributes_display()
    
    def show_choice_result(self, choice):
        """显示选择结果"""
        self.event_text.config(state='normal')
        self.event_text.delete(1.0, 'end')
        self.event_text.insert('end', f"✅ 选择结果\n\n")
        self.event_text.insert('end', f"{choice['description']}\n\n")
        #self.event_text.insert('end', "点击下方按钮继续你的冒险...")
        self.event_text.config(state='disabled')
        
        # 更新选择按钮为继续按钮
        self.show_continue_button()
    
    def show_continue_button(self):
        """显示继续按钮"""
        # 清除现有按钮
        for widget in self.choice_frame.winfo_children():
            widget.destroy()
        
        # 创建继续按钮
        continue_button = tk.Button(
            self.choice_frame,
            text="🚀 继续冒险",
            font=("Arial", 14, "bold"),
            bg='#27ae60',
            fg='white',
            relief='raised',
            bd=3,
            command=self.continue_adventure,
            height=3
        )
        continue_button.pack(fill='x', pady=10)
    
    def continue_adventure(self):
        """继续冒险，显示下一个随机事件"""
        self.add_log("继续冒险...")
        
        # 检查是否需要触发boss战斗
        if self.choice_count >= 3:
            self.add_log("⚠️ 你感受到了强大的威胁...")
            self.start_boss_battle()
        else:
            self.show_random_event()
    
    def calculate_battle_stats(self):
        """计算战斗属性"""
        # 血量 = 体质 * 5
        battle_health = self.attributes['体质'] * 5
        # 魔法上限 = 智力 * 5
        battle_magic = self.attributes['智力'] * 5
        # 攻击力 = 情商 * 1
        battle_attack = self.attributes['情商']
        # 闪避概率 = 幸运 * 2%
        battle_dodge = self.attributes['幸运'] * 2
        
        return {
            'health': battle_health,
            'magic': battle_magic,
            'attack': battle_attack,
            'dodge': battle_dodge
        }
    
    def start_boss_battle(self):
        """开始boss战斗"""
        # 计算玩家战斗属性
        player_stats = self.calculate_battle_stats()
        
        # Boss属性
        boss_stats = {
            'health': 100,
            'attack': 10,
            'dodge': 0
        }
        
        # 重置选择计数
        self.choice_count = 0
        
        # 创建战斗窗口
        self.create_battle_window(player_stats, boss_stats)
    
    def create_battle_window(self, player_stats, boss_stats):
        """创建战斗窗口"""
        # 创建新窗口
        self.battle_window = tk.Toplevel(self.root)
        self.battle_window.title("⚔️ Boss战斗")
        self.battle_window.geometry("800x600")
        self.battle_window.configure(bg='#2c3e50')
        self.battle_window.resizable(False, False)
        
        # 战斗状态
        self.battle_player_health = player_stats['health']
        self.battle_player_magic = player_stats['magic']
        self.battle_player_attack = player_stats['attack']
        self.battle_player_dodge = player_stats['dodge']
        
        self.battle_boss_health = boss_stats['health']
        self.battle_boss_attack = boss_stats['attack']
        self.battle_boss_dodge = boss_stats['dodge']
        
        self.battle_turn = 0  # 0=玩家回合，1=Boss回合
        
        # 创建战斗界面
        self.create_battle_interface()
        
        # 显示战斗开始信息
        self.add_battle_log("⚔️ Boss战斗开始！")
        self.add_battle_log(f"你的属性：血量{self.battle_player_health}，攻击{self.battle_player_attack}，闪避{self.battle_player_dodge}%")
        self.add_battle_log(f"Boss属性：血量{self.battle_boss_health}，攻击{self.battle_boss_attack}")
        self.add_battle_log("战斗开始！")
    
    def create_battle_interface(self):
        """创建战斗界面"""
        # 标题
        title_label = tk.Label(
            self.battle_window,
            text="⚔️ Boss战斗",
            font=("Arial", 24, "bold"),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        title_label.pack(pady=20)
        
        # 主框架
        main_frame = tk.Frame(self.battle_window, bg='#2c3e50')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # 左侧 - 战斗状态
        left_frame = tk.Frame(main_frame, bg='#34495e', relief='raised', bd=2)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # 玩家状态
        player_frame = tk.Frame(left_frame, bg='#34495e')
        player_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(
            player_frame,
            text="👤 玩家状态",
            font=("Arial", 16, "bold"),
            bg='#34495e',
            fg='#3498db'
        ).pack(anchor='w')
        
        self.player_health_label = tk.Label(
            player_frame,
            text=f"❤️ 血量: {self.battle_player_health}",
            font=("Arial", 12),
            bg='#34495e',
            fg='#e74c3c'
        )
        self.player_health_label.pack(anchor='w')
        
        self.player_magic_label = tk.Label(
            player_frame,
            text=f"🔮 魔法: {self.battle_player_magic}",
            font=("Arial", 12),
            bg='#34495e',
            fg='#9b59b6'
        )
        self.player_magic_label.pack(anchor='w')
        
        self.player_attack_label = tk.Label(
            player_frame,
            text=f"⚔️ 攻击: {self.battle_player_attack}",
            font=("Arial", 12),
            bg='#34495e',
            fg='#f39c12'
        )
        self.player_attack_label.pack(anchor='w')
        
        # Boss状态
        boss_frame = tk.Frame(left_frame, bg='#34495e')
        boss_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(
            boss_frame,
            text="👹 Boss状态",
            font=("Arial", 16, "bold"),
            bg='#34495e',
            fg='#e74c3c'
        ).pack(anchor='w')
        
        self.boss_health_label = tk.Label(
            boss_frame,
            text=f"❤️ 血量: {self.battle_boss_health}",
            font=("Arial", 12),
            bg='#34495e',
            fg='#e74c3c'
        )
        self.boss_health_label.pack(anchor='w')
        
        self.boss_attack_label = tk.Label(
            boss_frame,
            text=f"⚔️ 攻击: {self.battle_boss_attack}",
            font=("Arial", 12),
            bg='#34495e',
            fg='#f39c12'
        )
        self.boss_attack_label.pack(anchor='w')
        
        # 右侧 - 战斗日志和操作
        right_frame = tk.Frame(main_frame, bg='#34495e', relief='raised', bd=2)
        right_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        # 战斗日志
        tk.Label(
            right_frame,
            text="📝 战斗日志",
            font=("Arial", 16, "bold"),
            bg='#34495e',
            fg='#ecf0f1'
        ).pack(pady=15)
        
        self.battle_log_text = tk.Text(
            right_frame,
            height=20,
            width=40,
            font=("Arial", 10),
            bg='#2c3e50',
            fg='#ecf0f1',
            wrap='word',
            state='disabled'
        )
        self.battle_log_text.pack(padx=20, pady=10)
        
        # 战斗操作按钮
        self.battle_action_frame = tk.Frame(right_frame, bg='#34495e')
        self.battle_action_frame.pack(fill='x', padx=20, pady=10)
        
        # 攻击按钮
        self.attack_button = tk.Button(
            self.battle_action_frame,
            text="⚔️ 攻击",
            font=("Arial", 14, "bold"),
            bg='#e74c3c',
            fg='white',
            relief='raised',
            bd=3,
            command=self.player_attack,
            height=2
        )
        self.attack_button.pack(fill='x', pady=5)
        
        # 防御按钮
        self.defend_button = tk.Button(
            self.battle_action_frame,
            text="🛡️ 防御",
            font=("Arial", 14, "bold"),
            bg='#3498db',
            fg='white',
            relief='raised',
            bd=3,
            command=self.player_defend,
            height=2
        )
        self.defend_button.pack(fill='x', pady=5)
    
    def add_battle_log(self, message):
        """添加战斗日志"""
        self.battle_log_text.config(state='normal')
        self.battle_log_text.insert('end', f"{message}\n")
        self.battle_log_text.see('end')
        self.battle_log_text.config(state='disabled')
    
    def update_battle_display(self):
        """更新战斗显示"""
        self.player_health_label.config(text=f"❤️ 血量: {self.battle_player_health}")
        self.player_magic_label.config(text=f"🔮 魔法: {self.battle_player_magic}")
        self.player_attack_label.config(text=f"⚔️ 攻击: {self.battle_player_attack}")
        self.boss_health_label.config(text=f"❤️ 血量: {self.battle_boss_health}")
        self.boss_attack_label.config(text=f"⚔️ 攻击: {self.battle_boss_attack}")
    
    def player_attack(self):
        """玩家攻击"""
        # 检查闪避
        if random.randint(1, 100) <= self.battle_boss_dodge:
            self.add_battle_log("Boss闪避了你的攻击！")
        else:
            damage = self.battle_player_attack
            self.battle_boss_health -= damage
            self.add_battle_log(f"你对Boss造成了{damage}点伤害！")
        
        self.update_battle_display()
        
        # 检查Boss是否死亡
        if self.battle_boss_health <= 0:
            self.battle_boss_health = 0
            self.add_battle_log("🎉 你击败了Boss！")
            self.end_battle(True)
            return
        
        # Boss回合
        self.boss_turn()
    
    def player_defend(self):
        """玩家防御"""
        self.add_battle_log("你选择了防御，减少50%伤害")
        # Boss回合，但伤害减半
        self.boss_turn(defending=True)
    
    def boss_turn(self, defending=False):
        """Boss回合"""
        # 检查玩家闪避
        if random.randint(1, 100) <= self.battle_player_dodge:
            self.add_battle_log("你闪避了Boss的攻击！")
        else:
            damage = self.battle_boss_attack
            if defending:
                damage = damage // 2
                self.add_battle_log(f"Boss攻击了你，但由于防御只造成{damage}点伤害！")
            else:
                self.add_battle_log(f"Boss攻击了你，造成{damage}点伤害！")
            
            self.battle_player_health -= damage
        
        self.update_battle_display()
        
        # 检查玩家是否死亡
        if self.battle_player_health <= 0:
            self.battle_player_health = 0
            self.add_battle_log("💀 你被Boss击败了！")
            self.end_battle(False)
            return
        
        self.add_battle_log("轮到你的回合了...")
    
    def end_battle(self, victory):
        """结束战斗"""
        # 禁用战斗按钮
        self.attack_button.config(state='disabled')
        self.defend_button.config(state='disabled')
        
        if victory:
            self.add_battle_log("🎉 战斗胜利！你获得了经验奖励！")
            self.experience += 50
            self.add_log("Boss战斗胜利！获得50经验值")
        else:
            self.add_battle_log("💀 战斗失败！但你从中获得了经验...")
            self.experience += 20
            self.add_log("Boss战斗失败，获得20经验值")
        
        # 添加关闭按钮
        close_button = tk.Button(
            self.battle_action_frame,
            text="🚪 关闭战斗窗口",
            font=("Arial", 14, "bold"),
            bg='#27ae60',
            fg='white',
            relief='raised',
            bd=3,
            command=self.close_battle_window,
            height=2
        )
        close_button.pack(fill='x', pady=10)
        
        # 更新主游戏属性显示
        self.update_attributes_display()
    
    def close_battle_window(self):
        """关闭战斗窗口"""
        self.battle_window.destroy()
        # 继续游戏
        self.show_random_event()
    
    def create_attributes_display(self, parent):
        """创建属性显示区域"""
        # 属性标题
        attr_title = tk.Label(
            parent,
            text="📊 角色属性",
            font=("Arial", 16, "bold"),
            bg='#34495e',
            fg='#ecf0f1'
        )
        attr_title.pack(pady=15)
        
        # 属性显示框架
        self.attr_frame = tk.Frame(parent, bg='#34495e')
        self.attr_frame.pack(fill='x', padx=20, pady=10)
        
        # 创建属性标签
        self.attr_labels = {}
        for attr_name in self.attributes:
            label = tk.Label(
                self.attr_frame,
                text=f"{attr_name}: {self.attributes[attr_name]}",
                font=("Arial", 12),
                bg='#34495e',
                fg='#ecf0f1'
            )
            label.pack(anchor='w', pady=2)
            self.attr_labels[attr_name] = label
        
        # 生命值和魔法值显示
        self.health_label = tk.Label(
            self.attr_frame,
            text=f"❤️ 生命值: {self.health}/{self.max_health}",
            font=("Arial", 12),
            bg='#34495e',
            fg='#e74c3c'
        )
        self.health_label.pack(anchor='w', pady=2)
        
        self.magic_label = tk.Label(
            self.attr_frame,
            text=f"🔮 魔法值: {self.magic}/{self.max_magic}",
            font=("Arial", 12),
            bg='#34495e',
            fg='#9b59b6'
        )
        self.magic_label.pack(anchor='w', pady=2)
        
        self.exp_label = tk.Label(
            self.attr_frame,
            text=f"⭐ 经验值: {self.experience}",
            font=("Arial", 12),
            bg='#34495e',
            fg='#f39c12'
        )
        self.exp_label.pack(anchor='w', pady=2)
        
        self.choice_count_label = tk.Label(
            self.attr_frame,
            text=f"🎯 选择次数: {self.choice_count}/3",
            font=("Arial", 12),
            bg='#34495e',
            fg='#e67e22'
        )
        self.choice_count_label.pack(anchor='w', pady=2)
    
    def update_attributes_display(self):
        """更新属性显示"""
        for attr_name, value in self.attributes.items():
            self.attr_labels[attr_name].config(text=f"{attr_name}: {value}")
        
        self.health_label.config(text=f"❤️ 生命值: {self.health}/{self.max_health}")
        self.magic_label.config(text=f"🔮 魔法值: {self.magic}/{self.max_magic}")
        self.exp_label.config(text=f"⭐ 经验值: {self.experience}")
        self.choice_count_label.config(text=f"🎯 选择次数: {self.choice_count}/3")
    
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
            # 首先尝试JSON解析
            attr_dict = json.loads(attr_string)
            self.attributes.update(attr_dict)
            self.add_log(f"角色属性已加载：{attr_dict}")
            # 更新属性显示
            self.update_attributes_display()
        except json.JSONDecodeError:
            # 如果JSON解析失败，尝试使用ast.literal_eval（向后兼容）
            try:
                attr_dict = ast.literal_eval(attr_string)
                self.attributes.update(attr_dict)
                self.add_log(f"角色属性已加载（兼容模式）：{attr_dict}")
                self.update_attributes_display()
            except Exception as e:
                self.add_log(f"加载角色属性失败：{str(e)}")
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
