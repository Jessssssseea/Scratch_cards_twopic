import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

def load_image(file_path, label):
    try:
        img = Image.open(file_path)
        img.thumbnail((200, 200))  # 调整图片大小
        photo = ImageTk.PhotoImage(img)
        label.config(image=photo)
        label.image = photo  # 保持对图片的引用
    except Exception as e:
        None
        # messagebox.showerror("错误", f"加载图片时出错: {e}")

def show_current_images():
    current_dir = os.getcwd()
    background_path = os.path.join(current_dir, "background.png")
    scratch_path = os.path.join(current_dir, "scratch.png")
    
    # 预览当前文件夹中的图片
    load_image(background_path, background_label)
    load_image(scratch_path, scratch_label)

def select_background():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        entry_background.delete(0, tk.END)
        entry_background.insert(0, file_path)
        load_image(file_path, background_label)

def select_scratch():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        entry_scratch.delete(0, tk.END)
        entry_scratch.insert(0, file_path)
        load_image(file_path, scratch_label)

def save_images():
    background_path = entry_background.get()
    scratch_path = entry_scratch.get()


    try:
        if not background_path or not scratch_path:
            if not background_path:
                scratch_image = Image.open(scratch_path)
                scratch_image.save("scratch.png")
            if not scratch_path:
                background_image = Image.open(background_path)
                background_image.save("background.png")
        else:
            background_image = Image.open(background_path)
            scratch_image = Image.open(scratch_path)

            background_image.save("background.png")
            scratch_image.save("scratch.png")

        messagebox.showinfo("成功", f"图片已成功保存到当前目录: {os.getcwd()}")
        show_current_images()  # 更新预览
    except Exception as e:
        messagebox.showerror("错误", f"保存图片时出错: {e}")


# 创建主窗口
root = tk.Tk()
root.title("图片选择器")

# 背景图片选择
tk.Label(root, text="选择背景图片:").pack(pady=5)

background_label = tk.Label(root)
background_label.pack(pady=5)


entry_background = tk.Entry(root, width=50)
entry_background.pack(pady=5)
tk.Button(root, text="选择背景图片", command=select_background).pack(pady=5)

# 刮开图选择
tk.Label(root, text="选择刮开图片:").pack(pady=5)

scratch_label = tk.Label(root)
scratch_label.pack(pady=5)

entry_scratch = tk.Entry(root, width=50)
entry_scratch.pack(pady=5)
tk.Button(root, text="选择刮开图片", command=select_scratch).pack(pady=5)

# 保存按钮
tk.Button(root, text="保存图片", command=save_images).pack(pady=20)

show_current_images()  # 初始化显示当前文件夹中的图片


# 运行主循环
root.mainloop()
