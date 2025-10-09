# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import ast
import random
import json
import os
from boss_battle import BossBattleUI

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
        self.event_count = 0  # 事件计数器
        self.choice_event_count = 0  # 选择事件计数器
        self.last_negative_event = 0  # 上次负面事件的事件计数
        
        # 负面事件列表
        self.negative_events = [
            "拖延症发作", "懒惰成性", "社交恐惧症", "学习倦怠", 
            "身体健康问题", "网络成瘾", "人际关系破裂", "经济困难", "自我怀疑"
        ]
        
        # Boss状态（持久化）
        self.boss_max_health = 100
        self.boss_current_health = 100  # 持久化的boss血量
        
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
                # 处理有choices字段的事件
                if 'choices' in event_data:
                    for choice in event_data['choices']:
                        for effect_name, effect_value in choice['effects'].items():
                            if isinstance(effect_value, list) and len(effect_value) == 2:
                                choice['effects'][effect_name] = tuple(effect_value)
                
                # 处理auto_roll事件
                if 'auto_roll' in event_data:
                    auto_roll = event_data['auto_roll']
                    # 转换success_effects
                    for effect_name, effect_value in auto_roll.get('success_effects', {}).items():
                        if isinstance(effect_value, list) and len(effect_value) == 2:
                            auto_roll['success_effects'][effect_name] = tuple(effect_value)
                    # 转换failure_effects
                    for effect_name, effect_value in auto_roll.get('failure_effects', {}).items():
                        if isinstance(effect_value, list) and len(effect_value) == 2:
                            auto_roll['failure_effects'][effect_name] = tuple(effect_value)
            
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
        # 增加事件计数
        self.event_count += 1
        
        # 根据选择事件计数决定事件类型
        if self.choice_event_count >= 5:
            # 5次选择事件后，检查是否可以触发负面roll点事件
            can_trigger_negative = (
                random.random() < 0.15 and  # 15%概率
                self.event_count - self.last_negative_event >= 3  # 距离上次负面事件至少3次事件
            )
            
            if can_trigger_negative:
                # 选择负面roll点事件
                available_negative_events = [event for event in self.negative_events if event in self.event_library]
                if available_negative_events:
                    event_name = random.choice(available_negative_events)
                    self.last_negative_event = self.event_count  # 记录负面事件发生时间
                    self.add_log(f"触发第{self.event_count}次事件 - 负面roll点事件: {event_name}")
                else:
                    # 如果没有可用的负面事件，选择普通事件
                    positive_events = [event for event in self.event_library.keys() if event not in self.negative_events and 'choices' in self.event_library[event]]
                    if positive_events:
                        event_name = random.choice(positive_events)
                        self.add_log(f"触发第{self.event_count}次事件 - 选择事件: {event_name}")
                    else:
                        event_name = random.choice(list(self.event_library.keys()))
                        self.add_log(f"触发第{self.event_count}次事件: {event_name}")
            else:
                # 选择普通选择事件
                positive_events = [event for event in self.event_library.keys() if event not in self.negative_events and 'choices' in self.event_library[event]]
                if positive_events:
                    event_name = random.choice(positive_events)
                    self.add_log(f"触发第{self.event_count}次事件 - 选择事件: {event_name}")
                else:
                    # 如果没有正面事件，随机选择
                    event_name = random.choice(list(self.event_library.keys()))
                    self.add_log(f"触发第{self.event_count}次事件: {event_name}")
        else:
            # 前5次只选择普通选择事件
            positive_events = [event for event in self.event_library.keys() if event not in self.negative_events and 'choices' in self.event_library[event]]
            if positive_events:
                event_name = random.choice(positive_events)
                self.add_log(f"触发第{self.event_count}次事件 - 选择事件: {event_name}")
            else:
                # 如果没有正面事件，随机选择
                event_name = random.choice(list(self.event_library.keys()))
                self.add_log(f"触发第{self.event_count}次事件: {event_name}")
        
        self.current_event = self.event_library[event_name]
        
        # 显示事件描述
        self.event_text.config(state='normal')
        self.event_text.delete(1.0, 'end')
        if 'choices' in self.current_event:
            self.event_text.insert('end', f"🎮 {event_name} (第{self.event_count}次事件, 第{self.choice_event_count}次选择事件)\n\n")
        else:
            self.event_text.insert('end', f"🎮 {event_name} (第{self.event_count}次事件, Roll点事件)\n\n")
        self.event_text.insert('end', f"{self.current_event['description']}\n\n")
        
        # 检查是否是自动roll点事件
        if "auto_roll" in self.current_event:
            # 处理自动roll点事件
            self.handle_auto_roll_event(self.current_event)
            return
        else:
            # 普通事件，显示选择
            if "choices" in self.current_event:
                self.current_choices = self.current_event["choices"]
                self.event_text.insert('end', "请选择你的行动...")
                self.event_text.config(state='disabled')
                self.update_dynamic_choices()
            else:
                # 没有choices字段的事件，显示提示
                self.current_choices = []
                self.event_text.insert('end', "\n\n按任意键继续...")
                self.event_text.config(state='disabled')
    
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
        # 增加选择事件计数
        self.choice_event_count += 1
        
        # 应用效果并获取修改信息
        changes = self.apply_effects(choice["effects"])
        
        # 显示结果界面
        self.show_choice_result(choice, changes)
    
    def handle_auto_roll_event(self, event_data):
        """处理自动roll点事件"""
        auto_roll = event_data.get("auto_roll")
        if not auto_roll:
            return False
        
        # 增加选择计数
        self.choice_count += 1
        
        # 解析成功概率公式
        success_prob = self.calculate_success_probability(auto_roll["success_probability"])
        
        # 进行roll点
        roll_result = random.randint(1, 100)
        success = roll_result <= success_prob
        
        if success:
            # 成功效果
            changes = self.apply_effects(auto_roll["success_effects"])
            description = auto_roll["success_description"]
            self.add_log(f"🎯 Roll点成功！({roll_result}/{success_prob})")
        else:
            # 失败效果
            changes = self.apply_effects(auto_roll["failure_effects"])
            description = auto_roll["failure_description"]
            self.add_log(f"❌ Roll点失败！({roll_result}/{success_prob})")
        
        # 显示结果
        self.show_auto_roll_result(description, changes)
        return True
    
    def calculate_success_probability(self, formula):
        """计算成功概率"""
        try:
            # 替换公式中的属性名称为实际值
            formula_str = formula
            for attr_name, attr_value in self.attributes.items():
                formula_str = formula_str.replace(attr_name, str(attr_value))
            
            # 计算概率（限制在1-100之间）
            probability = eval(formula_str)
            return max(1, min(100, int(probability)))
        except:
            # 如果计算出错，返回默认概率
            return 50
    
    def apply_effects(self, effects):
        """应用选择效果，返回修改信息"""
        changes = []  # 存储所有修改信息
        
        for effect, value in effects.items():
            if effect in self.attributes:
                # 属性效果
                if isinstance(value, tuple):
                    change = random.randint(value[0], value[1])
                else:
                    change = value
                self.attributes[effect] += change
                changes.append(f"{effect} {change:+d} (当前: {self.attributes[effect]})")
                self.add_log(f"{effect} {change:+d} (当前: {self.attributes[effect]})")
            elif effect == "health":
                # 生命值效果
                if isinstance(value, tuple):
                    change = random.randint(value[0], value[1])
                else:
                    change = value
                self.health = min(self.max_health, self.health + change)
                changes.append(f"生命值 {change:+d} (当前: {self.health})")
                self.add_log(f"生命值 {change:+d} (当前: {self.health})")
            elif effect == "magic":
                # 魔法值效果
                if isinstance(value, tuple):
                    change = random.randint(value[0], value[1])
                else:
                    change = value
                self.magic = min(self.max_magic, self.magic + change)
                changes.append(f"魔法值 {change:+d} (当前: {self.magic})")
                self.add_log(f"魔法值 {change:+d} (当前: {self.magic})")
            elif effect == "experience":
                # 经验值效果
                if isinstance(value, tuple):
                    change = random.randint(value[0], value[1])
                else:
                    change = value
                self.experience += change
                changes.append(f"经验值 {change:+d} (当前: {self.experience})")
                self.add_log(f"经验值 {change:+d} (当前: {self.experience})")
        
        # 更新属性显示
        self.update_attributes_display()
        
        return changes
    
    def show_choice_result(self, choice, changes):
        """显示选择结果"""
        self.event_text.config(state='normal')
        self.event_text.delete(1.0, 'end')
        self.event_text.insert('end', f"✅ 选择结果\n\n")
        self.event_text.insert('end', f"{choice['description']}\n\n")
        
        # 显示属性修改
        if changes:
            self.event_text.insert('end', "📊 属性变化：\n")
            for change in changes:
                self.event_text.insert('end', f"• {change}\n")
            self.event_text.insert('end', "\n")
        
        self.event_text.config(state='disabled')
        
        # 更新选择按钮为继续按钮
        self.show_continue_button()
    
    def show_auto_roll_result(self, description, changes):
        """显示自动roll点结果"""
        self.event_text.config(state='normal')
        # 不清空现有内容，在现有内容基础上添加结果
        self.event_text.insert('end', f"\n🎲 自动Roll点结果\n\n")
        self.event_text.insert('end', f"{description}\n\n")
        
        # 显示属性修改
        if changes:
            self.event_text.insert('end', "📊 属性变化：\n")
            for change in changes:
                self.event_text.insert('end', f"• {change}\n")
            self.event_text.insert('end', "\n")
        
        self.event_text.config(state='disabled')
        
        # 显示继续按钮
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
        if self.choice_count >= 10:
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
        """开始boss战斗（委托至独立模块）"""
        # 重置选择计数
        self.choice_count = 0

        callbacks = {
            'on_log': self.add_log,
            'on_battle_end': self._on_boss_battle_end,
            'get_player_stats': self.calculate_battle_stats,
            'get_boss_persistent': self._get_boss_persistent,
            'set_boss_persistent': self._set_boss_persistent,
            'update_main_attributes': self.update_attributes_display,
            'on_continue_game': self.show_random_event,
        }

        # 实例化 Boss 战 UI（独立窗口）
        self.boss_battle_ui = BossBattleUI(self.root, callbacks)

    def _get_boss_persistent(self):
        return self.boss_current_health, self.boss_max_health

    def _set_boss_persistent(self, new_health):
        self.boss_current_health = max(0, min(self.boss_max_health, new_health))

    def _on_boss_battle_end(self, victory, boss_remaining_health, exp_delta):
        # 由 Boss 模块回调：同步经验与 Boss 血量
        self.experience += exp_delta
        self.boss_current_health = boss_remaining_health if boss_remaining_health > 0 else self.boss_max_health
        self.update_attributes_display()
    
    
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
            text=f"🎯 选择次数: {self.choice_count}/10",
            font=("Arial", 12),
            bg='#34495e',
            fg='#e67e22'
        )
        self.choice_count_label.pack(anchor='w', pady=2)
        
        # Boss血量显示
        self.boss_health_display_label = tk.Label(
            self.attr_frame,
            text=f"👹 Boss血量: {self.boss_current_health}/{self.boss_max_health}",
            font=("Arial", 12),
            bg='#34495e',
            fg='#e74c3c'
        )
        self.boss_health_display_label.pack(anchor='w', pady=2)
    
    def update_attributes_display(self):
        """更新属性显示"""
        for attr_name, value in self.attributes.items():
            self.attr_labels[attr_name].config(text=f"{attr_name}: {value}")
        
        self.health_label.config(text=f"❤️ 生命值: {self.health}/{self.max_health}")
        self.magic_label.config(text=f"🔮 魔法值: {self.magic}/{self.max_magic}")
        self.exp_label.config(text=f"⭐ 经验值: {self.experience}")
        self.choice_count_label.config(text=f"🎯 选择次数: {self.choice_count}/10")
        self.boss_health_display_label.config(text=f"👹 Boss血量: {self.boss_current_health}/{self.boss_max_health}")
    
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
