# -*- coding: utf-8 -*-
import tkinter as tk
import random


class BossBattleUI:
    """Boss 战斗窗口与逻辑，独立于主游戏。

    通过回调与宿主（GameMain）交互：
    - on_log(message): 写入主游戏日志
    - on_battle_end(victory, boss_remaining_health, exp_delta): 战斗结束回调
    - get_player_stats(): 返回玩家战斗属性 dict
    - get_boss_persistent(): 返回 (boss_current_health, boss_max_health)
    - set_boss_persistent(new_health): 持久化 Boss 当前血量
    - update_main_attributes(): 刷新主界面属性显示
    - on_continue_game(): 关闭后继续游戏/事件
    """

    def __init__(self, root, callbacks):
        self.root = root
        self.cb = callbacks

        player_stats = self.cb['get_player_stats']()
        boss_current, _ = self.cb['get_boss_persistent']()

        # 基础 Boss 配置（可按需扩展成参数）
        boss_stats = {
            'health': boss_current,
            'attack': 10,
            'dodge': 0,
        }

        # 初始化战斗状态
        self.battle_player_health = player_stats['health']
        self.battle_player_magic = player_stats['magic']
        self.battle_player_attack = player_stats['attack']
        self.battle_player_dodge = player_stats['dodge']

        self.battle_boss_health = boss_stats['health']
        self.battle_boss_attack = boss_stats['attack']
        self.battle_boss_dodge = boss_stats['dodge']

        self._build_window()
        self._build_interface()

        self.add_battle_log("⚔️ Boss战斗开始！")
        self.add_battle_log(
            f"你的属性：血量{self.battle_player_health}，攻击{self.battle_player_attack}，闪避{self.battle_player_dodge}%"
        )
        self.add_battle_log(
            f"Boss属性：血量{self.battle_boss_health}，攻击{self.battle_boss_attack}"
        )
        self.add_battle_log("战斗开始！")

    def _build_window(self):
        self.window = tk.Toplevel(self.root)
        self.window.title("⚔️ Boss战斗")
        self.window.geometry("800x600")
        self.window.configure(bg='#2c3e50')
        self.window.resizable(False, False)

    def _build_interface(self):
        title_label = tk.Label(
            self.window,
            text="⚔️ Boss战斗",
            font=("Arial", 24, "bold"),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        title_label.pack(pady=20)

        main_frame = tk.Frame(self.window, bg='#2c3e50')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)

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

        # Boss 状态
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

        # 右侧 日志 + 操作
        right_frame = tk.Frame(main_frame, bg='#34495e', relief='raised', bd=2)
        right_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))

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

        self.battle_action_frame = tk.Frame(right_frame, bg='#34495e')
        self.battle_action_frame.pack(fill='x', padx=20, pady=10)

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

    # ---- 逻辑与事件 ----
    def add_battle_log(self, message):
        self.battle_log_text.config(state='normal')
        self.battle_log_text.insert('end', f"{message}\n")
        self.battle_log_text.see('end')
        self.battle_log_text.config(state='disabled')

    def update_battle_display(self):
        self.player_health_label.config(text=f"❤️ 血量: {self.battle_player_health}")
        self.player_magic_label.config(text=f"🔮 魔法: {self.battle_player_magic}")
        self.player_attack_label.config(text=f"⚔️ 攻击: {self.battle_player_attack}")
        self.boss_health_label.config(text=f"❤️ 血量: {self.battle_boss_health}")
        self.boss_attack_label.config(text=f"⚔️ 攻击: {self.battle_boss_attack}")

    def player_attack(self):
        if random.randint(1, 100) <= self.battle_boss_dodge:
            self.add_battle_log("Boss闪避了你的攻击！")
        else:
            damage = self.battle_player_attack
            self.battle_boss_health -= damage
            self.add_battle_log(f"你对Boss造成了{damage}点伤害！")

        self.update_battle_display()

        if self.battle_boss_health <= 0:
            self.battle_boss_health = 0
            self.add_battle_log("🎉 你击败了Boss！")
            self.end_battle(True)
            return

        self.boss_turn()

    def player_defend(self):
        self.add_battle_log("你选择了防御，减少50%伤害")
        self.boss_turn(defending=True)

    def boss_turn(self, defending=False):
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

        if self.battle_player_health <= 0:
            self.battle_player_health = 0
            self.add_battle_log("💀 你被Boss击败了！")
            self.end_battle(False)
            return

        self.add_battle_log("轮到你的回合了...")

    def end_battle(self, victory):
        # 同步持久化 Boss 血量
        self.cb['set_boss_persistent'](self.battle_boss_health)

        # 禁用战斗按钮
        self.attack_button.config(state='disabled')
        self.defend_button.config(state='disabled')

        if victory:
            self.add_battle_log("🎉 战斗胜利！你获得了经验奖励！")
            exp_delta = 50
            self.cb['on_log']("Boss战斗胜利！获得50经验值")
            # Boss 被击败则重置血量
            boss_current, boss_max = self.cb['get_boss_persistent']()
            if self.battle_boss_health <= 0:
                self.cb['set_boss_persistent'](boss_max)
                self.add_battle_log("Boss已被击败，血量已重置！")
        else:
            self.add_battle_log("💀 战斗失败！但你从中获得了经验...")
            exp_delta = 20
            self.cb['on_log']("Boss战斗失败，获得20经验值")
            self.add_battle_log(f"Boss剩余血量：{self.battle_boss_health}")

        # 通知宿主经验变化
        self.cb['on_battle_end'](victory, self.battle_boss_health, exp_delta)
        self.cb['update_main_attributes']()

        close_button = tk.Button(
            self.battle_action_frame,
            text="🚪 关闭战斗窗口",
            font=("Arial", 14, "bold"),
            bg='#27ae60',
            fg='white',
            relief='raised',
            bd=3,
            command=self.close_window,
            height=2
        )
        close_button.pack(fill='x', pady=10)

    def close_window(self):
        self.window.destroy()
        # 回到宿主继续随机事件
        self.cb['on_continue_game']()


