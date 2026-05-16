import tkinter as tk
from tkinter import ttk, messagebox
import threading

from core.typing_engine import type_text
from core.controller import Controller
from core.settings_manager import load_settings

# ---------------- SETTINGS ---------------- #

settings = load_settings()

# ---------------- CONTROLLER ---------------- #

controller = Controller()

# ---------------- MAIN WINDOW ---------------- #

root = tk.Tk()

root.title("TypeMimic - Human Typing Simulator")

root.geometry("950x650")

root.configure(bg="#0f172a")

# ---------------- STYLE ---------------- #

style = ttk.Style()

style.theme_use("clam")

style.configure(
    "TButton",
    font=("Segoe UI", 11, "bold"),
    padding=10
)

style.configure(
    "Title.TLabel",
    background="#0f172a",
    foreground="white",
    font=("Segoe UI", 24, "bold")
)

style.configure(
    "Sub.TLabel",
    background="#0f172a",
    foreground="#cbd5e1",
    font=("Segoe UI", 10)
)

# ---------------- FUNCTIONS ---------------- #

typing_thread = None


def update_live_count(event=None):

    text = text_box.get("1.0", tk.END)

    words = len(text.split())

    chars = len(text.strip())

    count_label.config(
        text=f"Words: {words} | Characters: {chars}"
    )


def start_typing():

    global typing_thread

    text = text_box.get(
        "1.0",
        tk.END
    ).strip()

    if not text:

        messagebox.showwarning(
            "Warning",
            "Please enter text first."
        )

        return

    # Reset states
    controller.reset()

    status_label.config(
        text="Typing starts in 3 seconds...",
        fg="#22c55e"
    )

    # Start typing thread
    typing_thread = threading.Thread(
        target=type_text,
        args=(text, controller),
        daemon=True
    )

    typing_thread.start()


def pause_typing():

    controller.toggle_pause()

    if controller.paused:

        status_label.config(
            text="Typing Paused",
            fg="#facc15"
        )

    else:

        status_label.config(
            text="Typing Resumed",
            fg="#22c55e"
        )


def stop_typing():

    controller.stop_typing()

    status_label.config(
        text="Typing Stopped",
        fg="#ef4444"
    )


def clear_text():

    text_box.delete("1.0", tk.END)

    update_live_count()

    status_label.config(
        text="Text Cleared",
        fg="white"
    )


def paste_text():

    try:

        clipboard = root.clipboard_get()

        text_box.insert(
            tk.END,
            clipboard
        )

        update_live_count()

    except:

        pass


# ---------------- HEADER ---------------- #

header_frame = tk.Frame(
    root,
    bg="#0f172a"
)

header_frame.pack(pady=20)

title = ttk.Label(
    header_frame,
    text="⌨️ TypeMimic",
    style="Title.TLabel"
)

title.pack()

subtitle = ttk.Label(
    header_frame,
    text="Advanced Human-Like Typing Automation Tool",
    style="Sub.TLabel"
)

subtitle.pack()

# ---------------- MAIN FRAME ---------------- #

main_frame = tk.Frame(
    root,
    bg="#0f172a"
)

main_frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=10
)

# ---------------- TEXT FRAME ---------------- #

text_frame = tk.Frame(
    main_frame,
    bg="#1e293b",
    bd=2,
    relief="ridge"
)

text_frame.pack(
    fill="both",
    expand=True
)

# ---------------- TEXT BOX ---------------- #

text_box = tk.Text(
    text_frame,
    wrap="word",
    font=("Consolas", 12),
    bg="#111827",
    fg="white",
    insertbackground="white",
    relief="flat",
    padx=15,
    pady=15
)

text_box.pack(
    fill="both",
    expand=True
)

# Live count update
text_box.bind(
    "<KeyRelease>",
    update_live_count
)

# ---------------- CONTROL PANEL ---------------- #

control_frame = tk.Frame(
    root,
    bg="#0f172a"
)

control_frame.pack(pady=15)

# Start
ttk.Button(
    control_frame,
    text="▶ Start",
    command=start_typing
).grid(row=0, column=0, padx=10)

# Pause
ttk.Button(
    control_frame,
    text="⏸ Pause",
    command=pause_typing
).grid(row=0, column=1, padx=10)

# Stop
ttk.Button(
    control_frame,
    text="⛔ Stop",
    command=stop_typing
).grid(row=0, column=2, padx=10)

# Clear
ttk.Button(
    control_frame,
    text="🗑 Clear",
    command=clear_text
).grid(row=0, column=3, padx=10)

# Paste
ttk.Button(
    control_frame,
    text="📋 Paste",
    command=paste_text
).grid(row=0, column=4, padx=10)

# ---------------- SETTINGS PANEL ---------------- #

settings_frame = tk.Frame(
    root,
    bg="#1e293b",
    pady=10
)

settings_frame.pack(
    fill="x",
    padx=20
)

# Speed Label
tk.Label(
    settings_frame,
    text="Typing Speed:",
    bg="#1e293b",
    fg="white",
    font=("Segoe UI", 10, "bold")
).grid(row=0, column=0, padx=10)

# Speed Slider
speed_slider = tk.Scale(
    settings_frame,
    from_=1,
    to=10,
    orient="horizontal",
    bg="#1e293b",
    fg="white",
    troughcolor="#334155",
    highlightthickness=0
)

speed_slider.set(
    settings["typing_speed"]
)

speed_slider.grid(
    row=0,
    column=1
)

# Human Mode
human_mode = tk.BooleanVar(
    value=settings["human_mode"]
)

human_checkbox = tk.Checkbutton(
    settings_frame,
    text="Human Mode",
    variable=human_mode,
    bg="#1e293b",
    fg="white",
    selectcolor="#1e293b",
    activebackground="#1e293b"
)

human_checkbox.grid(
    row=0,
    column=2,
    padx=20
)

# ---------------- STATUS BAR ---------------- #

status_frame = tk.Frame(
    root,
    bg="#111827"
)

status_frame.pack(
    fill="x",
    side="bottom"
)

status_label = tk.Label(
    status_frame,
    text="Ready",
    bg="#111827",
    fg="white",
    anchor="w",
    padx=15,
    pady=8,
    font=("Segoe UI", 10)
)

status_label.pack(side="left")

count_label = tk.Label(
    status_frame,
    text="Words: 0 | Characters: 0",
    bg="#111827",
    fg="#cbd5e1",
    anchor="e",
    padx=15,
    pady=8,
    font=("Segoe UI", 10)
)

count_label.pack(side="right")

# ---------------- START GUI ---------------- #

def start_gui():

    root.mainloop()