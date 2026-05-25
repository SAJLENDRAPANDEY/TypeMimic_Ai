import tkinter as tk
from tkinter import ttk, messagebox
import threading
import os

from gui.themes import THEMES

from core.path_helper import resource_path

from core.settings_manager import (
    save_custom_profile,
    delete_custom_profile,
    update_custom_profile,
    load_settings,
    save_settings,
)

from core.typing_engine import type_text
from core.controller import Controller
from core.profiles import PROFILES

# ---------------- SETTINGS ---------------- #
settings = load_settings()
current_theme = THEMES.get(settings.get("theme", "Dark"), THEMES["Dark"])

# ---------------- CONTROLLER ---------------- #
controller = Controller()

# ---------------- MAIN WINDOW ---------------- #
root = tk.Tk()

# Window icon (keep a reference)
if os.path.exists(
    resource_path(
        "assets/logo.png"
    )
):

    logo_image = tk.PhotoImage(
        file=resource_path(
            "assets/logo.png"
        )
    )
    try:
        root.iconphoto(False, _logo)
    except Exception:
        pass

root.title("TypeMimicAi - Human Typing Simulator")
root.geometry("980x700")
root.minsize(820, 540)
root.configure(bg=current_theme["bg"])
root.resizable(True, True)

# Use grid exclusively on root-level widgets
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=0)  # header
root.grid_rowconfigure(1, weight=1)  # main
root.grid_rowconfigure(2, weight=0)  # control
root.grid_rowconfigure(3, weight=0)  # status

# ---------------- STYLE ---------------- #
style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Primary.TButton",
    background="#0ea5a3",
    foreground="white",
    font=("Segoe UI", 10, "bold"),
    padding=(10, 8),
    borderwidth=0,
)
style.map("Primary.TButton", background=[("active", "#089d97")])

style.configure("Warning.TButton", background="#f97316", foreground="white")
style.configure("Danger.TButton", background="#ef4444", foreground="white")
style.configure("Clear.TButton", background="#334155", foreground="white")
style.configure("Ghost.TButton", background="#374151", foreground="white")

# ---------------- FUNCTIONS / LOGIC ---------------- #
typing_thread = None
is_typing = False

# Placeholder text
placeholder = "Type or paste your text here..."

# ---------- Profile creator ----------

def open_profile_creator():
    profile_window = tk.Toplevel(root)
    profile_window.title("Create Custom Profile")
    profile_window.geometry("420x480")
    profile_window.configure(bg=current_theme["bg"]) 

    tk.Label(profile_window, text="Custom Profile Creator", bg=current_theme["bg"], fg=current_theme["fg"], font=("Segoe UI", 14, "bold")).pack(pady=12)

    tk.Label(profile_window, text="Profile Name", bg=current_theme["bg"], fg=current_theme["fg"]).pack()
    name_entry = tk.Entry(profile_window, font=("Segoe UI", 11))
    name_entry.pack(pady=6)

    tk.Label(profile_window, text="Typing Speed", bg=current_theme["bg"], fg=current_theme["fg"]).pack()
    speed_slider = tk.Scale(profile_window, from_=1, to=10, orient="horizontal")
    speed_slider.set(5)
    speed_slider.pack()

    tk.Label(profile_window, text="Error Rate", bg=current_theme["bg"], fg=current_theme["fg"]).pack()
    error_slider = tk.Scale(profile_window, from_=0, to=20, orient="horizontal")
    error_slider.set(3)
    error_slider.pack()

    sound_var = tk.BooleanVar(value=True)
    tk.Checkbutton(profile_window, text="Enable Sound", variable=sound_var, bg=current_theme["bg"], fg=current_theme["fg"], selectcolor=current_theme.get("panel", "#0f172a")).pack(pady=8)

    pause_var = tk.BooleanVar(value=True)
    tk.Checkbutton(profile_window, text="Enable Thinking Pause", variable=pause_var, bg=current_theme["bg"], fg=current_theme["fg"], selectcolor=current_theme.get("panel", "#0f172a")).pack()

    def save_profile():
        name = name_entry.get().strip()
        if not name:
            messagebox.showwarning("Warning", "Enter profile name")
            return
        speed = speed_slider.get()
        profile_data = {
            "min_delay": 0.01 * speed,
            "max_delay": 0.03 * speed,
            "error_rate": error_slider.get() / 100,
            "sound": sound_var.get(),
            "thinking_pause": pause_var.get(),
        }
        save_custom_profile(name, profile_data)
        # refresh dropdown values if dropdown exists
        try:
            profile_dropdown["values"] = list(PROFILES.keys()) + [name]
        except Exception:
            pass
        messagebox.showinfo("Saved", "Custom profile saved!")
        profile_window.destroy()

    ttk.Button(profile_window, text="Save Profile", command=save_profile).pack(pady=14)


# ---------- Statistics ----------

def update_statistics():
    try:
        characters_label.config(text=f"Characters Typed: {controller.characters_typed}")
        corrections_label.config(text=f"Corrections: {controller.corrections}")
        errors_label.config(text=f"Errors: {controller.errors}")
        duration_label.config(text=f"Duration: {controller.typing_duration()} sec")
        speed_label.config(text=f"Average Speed: {controller.average_speed()} cps")
    except Exception:
        pass
    root.after(500, update_statistics)


# ---------- Profile edit/delete ----------

def delete_selected_profile():
    selected = profile_var.get()
    default_profiles = ["Human Slow", "Student", "Fast Typist", "Programmer", "Careless Typist"]
    if selected in default_profiles:
        messagebox.showwarning("Protected", "Default profiles cannot be deleted.")
        return
    confirm = messagebox.askyesno("Delete Profile", f"Delete '{selected}' profile?")
    if not confirm:
        return
    delete_custom_profile(selected)
    values = list(profile_dropdown["values"]) if profile_dropdown and "values" in profile_dropdown.keys() else []
    if selected in values:
        values.remove(selected)
    try:
        profile_dropdown["values"] = values
        profile_var.set(values[0] if values else "Human Slow")
    except Exception:
        pass
    messagebox.showinfo("Deleted", "Profile deleted successfully.")


def edit_selected_profile():
    selected = profile_var.get()
    settings_local = load_settings()
    custom_profiles = settings_local.get("custom_profiles", {})
    if selected not in custom_profiles:
        messagebox.showwarning("Protected", "Only custom profiles can be edited.")
        return
    profile = custom_profiles[selected]

    profile_window = tk.Toplevel(root)
    profile_window.title("Edit Profile")
    profile_window.geometry("420x480")
    profile_window.configure(bg=current_theme["bg"]) 

    tk.Label(profile_window, text="Edit Profile", bg=current_theme["bg"], fg=current_theme["fg"], font=("Segoe UI", 14, "bold")).pack(pady=12)
    tk.Label(profile_window, text="Typing Speed", bg=current_theme["bg"], fg=current_theme["fg"]).pack()
    speed_slider = tk.Scale(profile_window, from_=1, to=10, orient="horizontal")
    # derive slider from stored max_delay
    try:
        speed_slider.set(int(profile.get("max_delay", 0.03) * 50))
    except Exception:
        speed_slider.set(5)
    speed_slider.pack()

    tk.Label(profile_window, text="Error Rate", bg=current_theme["bg"], fg=current_theme["fg"]).pack()
    error_slider = tk.Scale(profile_window, from_=0, to=20, orient="horizontal")
    try:
        error_slider.set(int(profile.get("error_rate", 0.03) * 100))
    except Exception:
        error_slider.set(3)
    error_slider.pack()

    sound_var = tk.BooleanVar(value=profile.get("sound", True))
    tk.Checkbutton(profile_window, text="Enable Sound", variable=sound_var, bg=current_theme["bg"], fg=current_theme["fg"], selectcolor=current_theme.get("panel", "#0f172a")).pack(pady=8)

    pause_var = tk.BooleanVar(value=profile.get("thinking_pause", True))
    tk.Checkbutton(profile_window, text="Enable Thinking Pause", variable=pause_var, bg=current_theme["bg"], fg=current_theme["fg"], selectcolor=current_theme.get("panel", "#0f172a")).pack()

    def save_edit():
        speed = speed_slider.get()
        updated_profile = {
            "min_delay": 0.01 * speed,
            "max_delay": 0.03 * speed,
            "error_rate": error_slider.get() / 100,
            "sound": sound_var.get(),
            "thinking_pause": pause_var.get(),
        }
        update_custom_profile(selected, updated_profile)
        messagebox.showinfo("Updated", "Profile updated successfully.")
        profile_window.destroy()

    ttk.Button(profile_window, text="Save Changes", command=save_edit).pack(pady=12)


# ---------- Theme / UI helpers ----------

def apply_theme(theme_name):
    theme = THEMES.get(theme_name, THEMES["Dark"])
    root.configure(bg=theme["bg"]) 

    # Header
    header_frame.configure(bg=theme["bg"]) 
    brand_col.configure(bg=theme["bg"]) 
    badge_frame.configure(bg=theme["bg"]) 

    # Main
    main_frame.configure(bg=theme["bg"]) 
    left_pane.configure(bg=theme["bg"])
    right_pane.configure(bg=theme["bg"]) 

    # Control & status
    control_frame.configure(bg=theme["panel"]) 
    inner_ctrl.configure(bg=theme["panel"]) 
    status_frame.configure(bg=theme["panel"]) 
    status_inner.configure(bg=theme["panel"]) 

    # Text area
    text_frame.configure(bg=theme["panel"]) 
    text_box.configure(bg=theme["text_bg"], fg=theme["fg"], insertbackground=theme["fg"], selectbackground=theme.get("accent", "#0ea5a3"))

    # Header labels
    try:
        title.configure(bg=theme["bg"], fg=theme["fg"]) 
        subtitle.configure(bg=theme["bg"], fg=theme.get("muted", "#94a3b8"))
    except Exception:
        pass

    # Status
    status_label.configure(bg=theme["panel"], fg=theme["fg"]) 
    count_label.configure(bg=theme["panel"], fg=theme["fg"]) 

    # Cards
    cards = [profile_card, speed_card, options_card, stats_card, theme_card]
    for card in cards:
        try:
            card.configure(bg=theme["panel"]) 
            for widget in card.winfo_children():
                if isinstance(widget, tk.Label):
                    widget.configure(bg=theme["panel"], fg=theme["fg"]) 
                elif isinstance(widget, tk.Frame):
                    widget.configure(bg=theme["panel"]) 
                    for child in widget.winfo_children():
                        if isinstance(child, tk.Label):
                            child.configure(bg=theme["panel"], fg=theme["fg"]) 
                        elif isinstance(child, tk.Checkbutton):
                            child.configure(bg=theme["panel"], fg=theme["fg"], activebackground=theme["panel"]) 
        except Exception:
            pass


def update_live_count(event=None):
    text = text_box.get("1.0", tk.END)
    words = len(text.split())
    chars = len(text.strip())
    count_label.config(text=f"  {words} words   {chars} chars  ")


def start_typing():
    global typing_thread, is_typing
    if is_typing:
        messagebox.showinfo("Typing Running", "Typing is already running.")
        return
    text = text_box.get("1.0", tk.END).strip()
    if not text or text == placeholder:
        messagebox.showwarning("Warning", "Please enter text first.")
        return
    is_typing = True
    start_button.config(state="disabled")
    controller.reset()
    _set_status("Typing starts in 3 seconds...", "#0d9488")
    selected_profile = profile_var.get()
    profile_data = PROFILES.get(selected_profile, {})
    typing_thread = threading.Thread(target=run_typing, args=(text, profile_data), daemon=True)
    typing_thread.start()


def run_typing(text, profile_data):
    global is_typing
    try:
        type_text(text, controller, profile_data)
        _set_status("✓  Typing completed", "#0d9488")
    except Exception as e:
        _set_status(f"Error: {e}", "#ef4444")
    finally:
        is_typing = False
        start_button.config(state="normal")


def pause_typing():
    controller.toggle_pause()
    if controller.paused:
        _set_status("⏸  Typing paused", "#f97316")
    else:
        _set_status("▶  Typing resumed", "#0d9488")


def stop_typing():
    global is_typing
    controller.stop_typing()
    is_typing = False
    start_button.config(state="normal")
    _set_status("⛔  Typing stopped", "#ef4444")


def clear_text():
    text_box.delete("1.0", tk.END)
    update_live_count()
    _set_status("Text cleared", "#94a3b8")


def paste_text():
    try:
        clipboard = root.clipboard_get()
        text_box.insert(tk.END, clipboard)
        update_live_count()
    except Exception:
        pass


def _set_status(msg, color):
    try:
        status_label.config(text=f"  {msg}", fg=color)
    except Exception:
        pass


# ---------------- LAYOUT HELPERS ---------------- #

def _divider(parent, pady=(0, 0)):
    frame = tk.Frame(parent, height=1, bg="#22252b")
    frame.pack(fill="x", pady=pady)
    return frame


def _section_card(parent, title_text):
    card = tk.Frame(parent, bg="#0f1720", highlightbackground="#1f2937", highlightthickness=1, padx=12, pady=10)
    card.pack(fill="x", pady=(0, 10))
    tk.Label(card, text=title_text, bg="#0f1720", fg="#94a3b8", font=("Segoe UI", 9, "bold"), anchor="w").pack(fill="x", pady=(0, 8))
    return card


# ═══════════════════════════════════════════════
#  HEADER (fixed)
# ═══════════════════════════════════════════════
header_frame = tk.Frame(root, bg=current_theme["bg"], height=76)
header_frame.grid(row=0, column=0, sticky="ew", padx=14, pady=(12, 6))
header_frame.grid_propagate(False)

brand_col = tk.Frame(header_frame, bg=current_theme["bg"])
brand_col.pack(side="left", padx=(6, 12))

if os.path.exists(
    resource_path(
        "assets/logo.png"
    )
):

    logo_image = tk.PhotoImage(
        file=resource_path(
            "assets/logo.png"
        )
    )
    try:
        logo_image = logo_image.subsample(15, 15)
    except Exception:
        pass
    logo_label = tk.Label(header_frame, image=logo_image, bg=current_theme["bg"]) 
    logo_label.image = logo_image
    logo_label.pack(side="left", padx=(8, 12))

title = tk.Label(brand_col, text="TypeMimicAi", bg=current_theme["bg"], fg=current_theme["fg"], font=("Segoe UI", 20, "bold"))
title.pack(anchor="w")
subtitle = tk.Label(brand_col, text="Human-Like Typing Automation", bg=current_theme["bg"], fg=current_theme.get("muted", "#94a3b8"), font=("Segoe UI", 10))
subtitle.pack(anchor="w")

badge_frame = tk.Frame(header_frame, bg=current_theme["bg"])
badge_frame.pack(side="right", padx=8)
tk.Label(badge_frame, text="v2.0", bg="#0ea5a3", fg="white", font=("Segoe UI", 9, "bold"), padx=8, pady=4).pack()

# ═══════════════════════════════════════════════
#  MAIN (expandable)
# ═══════════════════════════════════════════════
main_frame = tk.Frame(root, bg=current_theme["bg"] )
main_frame.grid(row=1, column=0, sticky="nsew", padx=12, pady=(6, 8))
main_frame.grid_columnconfigure(0, weight=3)
main_frame.grid_columnconfigure(1, weight=0)
main_frame.grid_columnconfigure(2, weight=0, minsize=320)
main_frame.grid_rowconfigure(0, weight=1)

# ── LEFT: editor pane ──
left_pane = tk.Frame(main_frame, bg=current_theme["bg"] )
left_pane.grid(row=0, column=0, sticky="nsew", padx=(6, 6), pady=6)

tk.Label(left_pane, text="INPUT TEXT", bg=current_theme["bg"], fg=current_theme.get("muted", "#94a3b8"), font=("Segoe UI", 8, "bold"), anchor="w").pack(fill="x", pady=(0, 8))

text_frame = tk.Frame(left_pane, bg=current_theme["panel"], highlightbackground="#1f2937", highlightthickness=1)
text_frame.pack(fill="both", expand=True)

text_box = tk.Text(text_frame, wrap="word", font=("Consolas", 12), bg=current_theme["text_bg"], fg=current_theme["fg"], insertbackground=current_theme["fg"], relief="flat", padx=14, pady=12, spacing3=3, undo=True)
v_scroll = ttk.Scrollbar(text_frame, orient="vertical", command=text_box.yview)
text_box.configure(yscrollcommand=v_scroll.set)
v_scroll.pack(side="right", fill="y")
text_box.pack(fill="both", expand=True, side="left")

text_box.insert("1.0", placeholder)
text_box.config(fg="#94a3b8")

def remove_placeholder(event):
    if text_box.get("1.0", "end-1c") == placeholder:
        text_box.delete("1.0", tk.END)
        text_box.config(fg=current_theme["fg"]) 

def add_placeholder(event):
    if not text_box.get("1.0", "end-1c").strip():
        text_box.insert("1.0", placeholder)
        text_box.config(fg="#94a3b8")

text_box.bind("<FocusIn>", remove_placeholder)
text_box.bind("<FocusOut>", add_placeholder)
text_box.bind("<KeyRelease>", update_live_count)

# ── Thin vertical divider ──
divider_frame = tk.Frame(main_frame, bg="#22252b", width=1)
divider_frame.grid(row=0, column=1, sticky="ns", padx=10, pady=6)

# ── RIGHT: settings sidebar ──
right_pane = tk.Frame(main_frame, bg=current_theme["bg"]) 
right_pane.grid(row=0, column=2, sticky="nsew", padx=(8,6), pady=6)
settings_frame = right_pane

# Profile card
profile_card = _section_card(right_pane, "TYPING PROFILE")
profile_var = tk.StringVar(value="Human Slow")
profile_dropdown = ttk.Combobox(profile_card, textvariable=profile_var, values=list(PROFILES.keys()), state="readonly", width=22, font=("Segoe UI", 10))
profile_dropdown.pack(fill="x")
try:
    profile_dropdown.current(0)
except Exception:
    pass

# Speed card
speed_card = _section_card(right_pane, "TYPING SPEED")
speed_row = tk.Frame(speed_card, bg="#0f1720")
speed_row.pack(fill="x")

tk.Label(speed_row, text="Slow", bg="#0f1720", fg=current_theme["fg"], font=("Segoe UI", 9)).pack(side="left")

speed_slider = tk.Scale(speed_row, from_=1, to=10, orient="horizontal", bg=current_theme["panel"], fg=current_theme["fg"], troughcolor="#263238", activebackground=current_theme.get("accent", "#0ea5a3"), highlightthickness=0, sliderrelief="flat", showvalue=False, length=120)
speed_slider.set(settings.get("typing_speed", 5))
speed_slider.pack(side="left", fill="x", expand=True, padx=8)

tk.Label(speed_row, text="Fast", bg="#0f1720", fg=current_theme["fg"], font=("Segoe UI", 9)).pack(side="left")

speed_val_label = tk.Label(speed_card, text=f"Level {settings.get('typing_speed',5)}", bg="#0f1720", fg=current_theme.get("accent", "#0ea5a3"), font=("Segoe UI", 10, "bold"))
speed_val_label.pack(fill="x", pady=(6, 0))

def _on_speed_change(val):
    speed_val_label.config(text=f"Level {val}")

speed_slider.config(command=_on_speed_change)

ttk.Button(profile_card, text="➕ Create Profile", command=open_profile_creator).pack(fill="x", pady=8)
ttk.Button(profile_card, text="✏ Edit Profile", command=edit_selected_profile).pack(fill="x", pady=(4,6))
ttk.Button(profile_card, text="🗑 Delete Profile", command=delete_selected_profile).pack(fill="x")

# Options card
options_card = _section_card(right_pane, "OPTIONS")

human_mode = tk.BooleanVar(value=settings.get("human_mode", True))

def _make_toggle(parent, text, variable):
    row = tk.Frame(parent, bg="#0f1720")
    row.pack(fill="x", pady=3)
    tk.Label(row, text=text, bg="#0f1720", fg=current_theme["fg"], font=("Segoe UI", 10)).pack(side="left")
    human_checkbox = tk.Checkbutton(row, variable=variable, bg="#0f1720", fg=current_theme["fg"], selectcolor=current_theme.get("panel","#0f1720"), activebackground="#0f1720", activeforeground=current_theme["fg"], relief="flat", cursor="hand2")
    human_checkbox.pack(side="right")
    return human_checkbox

human_checkbox = _make_toggle(options_card, "Human Mode", human_mode)

# STATISTICS CARD
stats_card = _section_card(right_pane, "TYPING STATISTICS")
characters_label = tk.Label(stats_card, text="Characters Typed: 0", bg="#0f1720", fg=current_theme["fg"], font=("Segoe UI", 10))
characters_label.pack(anchor="w", pady=2)
corrections_label = tk.Label(stats_card, text="Corrections: 0", bg="#0f1720", fg=current_theme["fg"], font=("Segoe UI", 10))
corrections_label.pack(anchor="w", pady=2)
errors_label = tk.Label(stats_card, text="Errors: 0", bg="#0f1720", fg=current_theme["fg"], font=("Segoe UI", 10))
errors_label.pack(anchor="w", pady=2)
duration_label = tk.Label(stats_card, text="Duration: 0 sec", bg="#0f1720", fg=current_theme["fg"], font=("Segoe UI", 10))
duration_label.pack(anchor="w", pady=2)
speed_label = tk.Label(stats_card, text="Average Speed: 0 cps", bg="#0f1720", fg=current_theme["fg"], font=("Segoe UI", 10))
speed_label.pack(anchor="w", pady=2)

# THEME SECTION
theme_card = _section_card(right_pane, "THEME")
theme_var = tk.StringVar(value=settings.get("theme", "Dark"))
theme_dropdown = ttk.Combobox(theme_card, textvariable=theme_var, values=list(THEMES.keys()), state="readonly", width=22, font=("Segoe UI", 10))
theme_dropdown.pack(fill="x")

def on_theme_change(event):
    selected_theme = theme_var.get()
    settings["theme"] = selected_theme
    save_settings(settings)
    apply_theme(selected_theme)

theme_dropdown.bind("<<ComboboxSelected>>", on_theme_change)

# ═══════════════════════════════════════════════
#  CONTROL TOOLBAR (fixed)
# ═══════════════════════════════════════════════
control_frame = tk.Frame(root, bg=current_theme.get("panel","#0b1220"), height=64)
control_frame.grid(row=2, column=0, sticky="ew", padx=8, pady=(0,4))
control_frame.grid_propagate(False)

inner_ctrl = tk.Frame(control_frame, bg=current_theme.get("panel","#0b1220"))
inner_ctrl.pack(padx=8, pady=8)

start_button = ttk.Button(inner_ctrl, text="▶  Start", style="Primary.TButton", command=start_typing)
start_button.grid(row=0, column=0, padx=(0,8))

pause_btn = ttk.Button(inner_ctrl, text="⏸  Pause", style="Warning.TButton", command=pause_typing)
pause_btn.grid(row=0, column=1, padx=6)

stop_btn = ttk.Button(inner_ctrl, text="⛔  Stop", style="Danger.TButton", command=stop_typing)
stop_btn.grid(row=0, column=2, padx=6)

sep = tk.Frame(inner_ctrl, width=1, bg="#263238")
sep.grid(row=0, column=3, padx=10, sticky="ns")

clear_btn = ttk.Button(inner_ctrl, text="🗑  Clear", style="Clear.TButton", command=clear_text)
clear_btn.grid(row=0, column=4, padx=6)

paste_btn = ttk.Button(inner_ctrl, text="📋  Paste", style="Ghost.TButton", command=paste_text)
paste_btn.grid(row=0, column=5, padx=(6,0))

# ═══════════════════════════════════════════════
#  STATUS BAR (fixed)
# ═══════════════════════════════════════════════
status_frame = tk.Frame(root, bg=current_theme.get("panel","#0b1220"), height=36)
status_frame.grid(row=3, column=0, sticky="ew", padx=0, pady=(0,4))
status_frame.grid_propagate(False)

_divider(status_frame, pady=(0,0))
status_inner = tk.Frame(status_frame, bg=current_theme.get("panel","#0b1220"))
status_inner.pack(fill="both", expand=True, padx=8)

status_label = tk.Label(status_inner, text="  Ready", bg=current_theme.get("panel","#0b1220"), fg=current_theme.get("muted", "#94a3b8"), anchor="w", padx=4, pady=4, font=("Segoe UI", 10))
status_label.pack(side="left")

count_label = tk.Label(status_inner, text="  0 words   0 chars  ", bg=current_theme.get("panel","#0b1220"), fg=current_theme.get("muted", "#94a3b8"), anchor="e", padx=4, pady=4, font=("Segoe UI", 9))
count_label.pack(side="right")

# Initialize theme and statistics loop
apply_theme(settings.get("theme", "Dark"))
update_statistics()

# ═══════════════════════════════════════════════
#  START GUI
# ═══════════════════════════════════════════════

def start_gui():
    root.mainloop()
