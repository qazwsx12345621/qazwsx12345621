import os
import time
import ctypes
import requests
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog

class WallpaperChanger:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Wallpaper Changer")
        self.root.geometry("500x600")
        self.count = 0
        self.interval = 60
        self.img_url_options = ["接口1", "接口2", "接口3", "接口4", "接口5", "接口6", "接口7", "少女写真"]
        self.img_url = tk.StringVar(self.root, self.img_url_options[0])  # 默认选择接口1
        self.custom_url = tk.StringVar(self.root, "")
        self.save_path = tk.StringVar(self.root, "")

        self.canvas = tk.Canvas(self.root, width=500, height=600)
        self.canvas.pack()

        self.label = tk.Label(self.canvas, text="Wallpaper Changer", font=("Arial", 20), fg="#336699")
        self.label.pack(pady=20)

        self.explain_label = tk.Label(self.canvas, text="这个程序基于选择的或自定义的图片URL来更换壁纸。",
                                      font=("Arial", 12), wraplength=380, fg="#333333")
        self.explain_label.pack()

        self.url_frame = tk.Frame(self.canvas)
        self.url_frame.pack()

        self.url_label = tk.Label(self.url_frame, text="自定义接口:", font=("Arial", 12), fg="#333333")
        self.url_label.pack(side=tk.LEFT)

        self.url_optionmenu = tk.OptionMenu(self.url_frame, self.img_url, *self.img_url_options)
        self.url_optionmenu.config(font=("Arial", 12))
        self.url_optionmenu.pack(side=tk.LEFT, padx=10)

        self.custom_url_frame = tk.Frame(self.canvas)
        self.custom_url_frame.pack()

        self.custom_url_label = tk.Label(self.custom_url_frame, text="自定义URL:", font=("Arial", 12), fg="#333333")
        self.custom_url_label.pack(side=tk.LEFT)

        self.custom_url_entry = tk.Entry(self.custom_url_frame, width=30, textvariable=self.custom_url, font=("Arial", 12))
        self.custom_url_entry.pack(side=tk.LEFT, padx=10)

        self.interval_frame = tk.Frame(self.canvas)
        self.interval_frame.pack()

        self.interval_label = tk.Label(self.interval_frame, text="间隔时间（秒）:", font=("Arial", 12), fg="#333333")
        self.interval_label.pack(side=tk.LEFT)

        self.interval_entry = tk.Entry(self.interval_frame, width=5, font=("Arial", 12))
        self.interval_entry.pack(side=tk.LEFT, padx=10)
        self.interval_entry.insert(0, self.interval)

        self.save_path_frame = tk.Frame(self.canvas)
        self.save_path_frame.pack()

        self.save_path_label = tk.Label(self.save_path_frame, text="保存路径:", font=("Arial", 12), fg="#333333")
        self.save_path_label.pack(side=tk.LEFT)

        self.save_path_entry = tk.Entry(self.save_path_frame, width=30, textvariable=self.save_path, font=("Arial", 12))
        self.save_path_entry.pack(side=tk.LEFT, padx=10)

        self.save_button = tk.Button(self.save_path_frame, text="保存壁纸", command=self.save_current_wallpaper,
                                     font=("Arial", 12), fg="#ffffff", bg="#336699")
        self.save_button.pack(side=tk.LEFT, padx=10)

        self.button_frame = tk.Frame(self.canvas)
        self.button_frame.pack()

        self.start_button = tk.Button(self.button_frame, text="开始", command=self.start_wallpaper_changer,
                                      font=("Arial", 12), fg="#ffffff", bg="#336699")
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.stop_button = tk.Button(self.button_frame, text="停止", command=self.stop_wallpaper_changer,
                                     font=("Arial", 12), fg="#ffffff", bg="#336699")
        self.stop_button.pack(side=tk.LEFT, padx=10)

        self.image_frame = tk.Frame(self.canvas)
        self.image_frame.pack(pady=20)

        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack()

        self.message_label = tk.Label(self.canvas, text="", font=("Arial", 12), fg="#ff0000")
        self.message_label.pack()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)  # 添加窗口关闭事件处理方法
        self.root.mainloop()

    def set_wallpaper(self, path):
        SPI_SETDESKWALLPAPER = 20
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, 0)

    def start_wallpaper_changer(self):
        self.interval = int(self.interval_entry.get())
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.change_wallpaper()

    def stop_wallpaper_changer(self):
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def change_wallpaper(self):
        img_url = self.img_url.get()
        custom_url = self.custom_url.get()

        if img_url == "接口1":
            img_url = "https://api.jczys.xyz/api/dmnh/index.php"
        elif img_url == "接口2":
            img_url = "https://api.jczys.xyz/api/sjwp/index.php"
        elif img_url == "接口3":
            img_url = "http://www.98qy.com/sjbz/api.php"
        elif img_url == "接口4":
            img_url = "https://t.mwm.moe/pc/"
        elif img_url == "接口5":
            img_url = "https://imgapi.xl0408.top/index.php"
        elif img_url == "接口6":
            img_url = "https://api.yimian.xyz/img"
        elif img_url == "接口7":
            img_url = "https://www.dmoe.cc/random.php"
        elif img_url == "少女写真":
            img_url = "https://www.hlapi.cn/api/mm2"

        if custom_url:
            img_url = custom_url

        try:
            response = requests.get(img_url, timeout=10)
            response.raise_for_status()
            self.download_image(response.content)
            img_path = os.path.join(os.getcwd(), "temp.jpg")
            self.set_wallpaper(img_path)
            self.count += 1
            self.show_image()
            self.message_label.config(text="")
        except requests.exceptions.RequestException:
            self.message_label.config(text="接口已失效")

        if self.stop_button["state"] == tk.NORMAL:
            self.root.after(self.interval * 1000, self.change_wallpaper)

    def download_image(self, content):
        with open('temp.jpg', 'wb') as file:
            file.write(content)

    def show_image(self):
        image = Image.open('temp.jpg')
        image = image.resize((300, 200), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        self.image_label.configure(image=photo)
        self.image_label.image = photo

    def on_closing(self):
        self.stop_wallpaper_changer()  # 停止壁纸切换
        self.root.destroy()  # 关闭窗口

    def save_current_wallpaper(self):
        img_path = os.path.join(os.getcwd(), "temp.jpg")

        save_dir = self.save_path.get()
        current_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
        save_file = os.path.join(save_dir, f"{current_time}.jpg")

        try:
            os.makedirs(save_dir, exist_ok=True)
            shutil.copyfile(img_path, save_file)
            self.message_label.config(text=f"保存成功：{save_file}", fg="#336699")
        except Exception as e:
            self.message_label.config(text=f"保存失败：{str(e)}", fg="#ff0000")

if __name__ == "__main__":
    WallpaperChanger()
