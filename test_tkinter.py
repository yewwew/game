# -*- coding: utf-8 -*-
try:
    import tkinter as tk
    print("tkinter导入成功")
    root = tk.Tk()
    root.title("测试")
    root.geometry("300x200")
    label = tk.Label(root, text="tkinter工作正常!")
    label.pack()
    root.mainloop()
except ImportError as e:
    print("导入失败:", e)
except Exception as e:
    print("其他错误:", e)
