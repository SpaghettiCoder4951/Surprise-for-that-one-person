import os
import sys
import ctypes
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


def resource_path(relative_path):
    # Works both when running normally and when bundled by PyInstaller
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, relative_path)


display_texts = [
    "HAII GFF",
    "Do you know what day it is today :o",
    "IT'S YOUR BDAYYY",
    "Ofc I diddd",
    "A collage of cutsie things kinda :3",
    "I put a bunch of our msgs togetha :D", 
    "And my goal is to make you cry >:D",
    "(Not sadge ones pls D:)",
    "So are you ready?",
    "Dis :D",
    "Heyyyy",
    "Yes you didd",
    "Pervvvv",
    "I-I wouldnt like that! Hmph!",
    "NUH UHH",
    "AAAAAAA",
    "Tooo baddd",
    "I LOVE YOUUU <3",
    "HEYYY",
    "BIGGER PERVV",
    "I LOVE YOURS MOREE",
    "LIARRR",
    "NOOOO",
    "I'D NEVERR",
    "Ofc I diddd <3",
    "Hehehehhee <3",
    "MEANIEEE",
    "That's all I have :D (This loops if you click :D)"
]

button_texts = [
    "HAII BFFF",
    "No bf what day is it :o",
    "Omg bf remembered :o",
    "So what's this supposed to be?",
    ":o",
    ":o",
    "D:",
    "YAEY :D",
    "HELL YEAAAHHH",
    "Bf still cute :3",
    "I didn't say that",
    "Ik it isssss",
    "Take it up the butt :3",
    "You're the cutesttt",
    "You're so preciousss",
    "Dat one embarassingggg",
    "I love you <3",
    "Mhm you're a girl hon <3",
    "Mpreg for my wife <3",
    "I love your voice <3",
    "Not me :3",
    "HEHEHE all trueee",
    "Bf had pervy thoughhttt",
    "HEYY YOU SAW THATT",
    "AAAAAA",
    "That's what you get <3",
    "HEYYY",
    "I LOVE YOU BOYFIEEE"
]

gif_paths = [
    "assets/seal.gif",
    "assets/usagi.gif", 
    "assets/mwah.gif",
    "assets/oror.gif",
    "assets/maomao.gif",
    "assets/fusion.gif",
    "assets/frieren.gif",
    "assets/sadge.gif",
    "assets/mashle.gif",
    "assets/cute.jpg",
    "assets/ovulating.jpg",
    "assets/season.jpg",
    "assets/perv.jpg",
    "assets/flirt.jpg",
    "assets/precious.jpg",
    "assets/marry.jpg",
    "assets/yearn.jpg",
    "assets/gfmakesmewife.jpg",
    "assets/mpreg.jpg",
    "assets/voice.jpg",
    "assets/horny.jpg",
    "assets/bebi.jpg",
    "assets/showa.jpg",
    "assets/jelly.jpg",
    "assets/newlyweds.jpg",
    "assets/tease.jpg",
    "assets/nap.jpg"
]

GIF_MAX_SIZE = (150, 150)  # Gif size

current_index = 0
current_animation_job = None  # Gif

# Loaded gifs in cache
loaded_gifs = {}


def set_titlebar_color(root, color_hex):
    # Windows bar color 
    if sys.platform != "win32":
        return  # only works on Windows

    root.update() 

    color_hex = color_hex.lstrip("#")
    r = int(color_hex[0:2], 16)
    g = int(color_hex[2:4], 16)
    b = int(color_hex[4:6], 16)
    colorref = (b << 16) | (g << 8) | r

    HWND = ctypes.windll.user32.GetParent(root.winfo_id())
    DWMWA_CAPTION_COLOR = 35  # Title bar color

    ctypes.windll.dwmapi.DwmSetWindowAttribute(
        HWND,
        DWMWA_CAPTION_COLOR,
        ctypes.byref(ctypes.c_int(colorref)),
        ctypes.sizeof(ctypes.c_int)
    )


def load_gif(path, max_size=None):
    if path in loaded_gifs:
        return loaded_gifs[path]

    gif = Image.open(resource_path(path))
    frames = []
    durations = []
    try:
        while True:
            frame = gif.copy()
            if max_size is not None:
                frame = frame.convert("RGBA")  # RGB setting
                frame.thumbnail(max_size)      # Resizing
            frames.append(ImageTk.PhotoImage(frame))
            durations.append(gif.info.get('duration', 100))
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass

    loaded_gifs[path] = (frames, durations)
    return frames, durations


def play_gif(path):
    global current_animation_job

    # Cancel the previous animation loop if one is running
    if current_animation_job is not None:
        root.after_cancel(current_animation_job)
        current_animation_job = None

    frames, durations = load_gif(path, GIF_MAX_SIZE)
    frame_index = 0

    def animate():
        nonlocal frame_index
        global current_animation_job
        canvas.itemconfig(gif_item, image=frames[frame_index])
        delay = durations[frame_index]
        frame_index = (frame_index + 1) % len(frames)
        current_animation_job = root.after(delay, animate)

    animate()


def next_state():
    global current_index
    current_index = (current_index + 1) % len(display_texts)

    canvas.itemconfig(text_item, text=display_texts[current_index])
    button.config(text=button_texts[current_index])

    # Wraps through gifs
    gif_index = current_index % len(gif_paths)
    play_gif(gif_paths[gif_index])


# Init
root = tk.Tk()
root.title("HAPPY BDAY GF :D")
root.iconbitmap(resource_path("assets/icon.ico"))
root.geometry("400x300")
root.resizable(False, False)

set_titlebar_color(root, "#adf16c")

# Canvas
canvas = tk.Canvas(root, width=400, height=300, highlightthickness=0, bd=0, bg="lightgreen")
canvas.pack(fill="both", expand=True)

# Text near top
text_item = canvas.create_text(200, 30, text=display_texts[0], font=("Segoe UI", 16), width=350, anchor="n")

# Gif placeholder (starts empty, filled in by play_gif below)
gif_item = canvas.create_image(200, 160, image="")

# Button placed on the canvas
button = tk.Button(
    root,
    text=button_texts[0],
    command=next_state,
    bg="#71daec",
    fg="black",
    activebackground="#4496e2",
    font=("Segoe UI", 11),
    relief="flat",       # No more goofy ass 3d lookin ass 5'11 thinking he 6 foot ass
    padx=10,
    pady=5
)

canvas.create_window(200, 260, window=button)

# Start the first gif on launch
play_gif(gif_paths[0])

root.mainloop()