<div align="center">

<img src="assets/logo.ico" alt="TypeMimic AI Logo" width="80" height="80"/>

# TypeMimic AI

**Human-Like Typing Automation for Desktop**

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Tkinter](https://img.shields.io/badge/GUI-Tkinter-informational?style=flat-square)](https://docs.python.org/3/library/tkinter.html)
[![PyAutoGUI](https://img.shields.io/badge/Automation-PyAutoGUI-orange?style=flat-square)](https://pyautogui.readthedocs.io/)
[![License](https://img.shields.io/badge/License-Educational-green?style=flat-square)](#license)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=flat-square)]()

[Features](#features) · [Installation](#installation) · [Usage](#usage) · [Project Structure](#project-structure) · [Build EXE](#build-exe) · [Roadmap](#roadmap)

</div>

---

## Overview

TypeMimic AI is a desktop automation tool that simulates natural, human-like typing behavior. It goes beyond simple keystroke injection by introducing realistic speed variation, natural pauses, typo generation with automatic correction, and configurable typing sound packs — all wrapped in a modern, theme-driven UI.

Built with Python and Tkinter, TypeMimic AI is designed for productivity workflows, UI testing, demo recordings, and any scenario where robotic instant-pasting falls short.

---

## Features

### Human-Like Typing Engine
- Realistic per-character delays with natural speed variation
- Burst typing behavior and human hesitation simulation
- Configurable pauses after punctuation, line breaks, and paragraphs

### Typo & Correction Simulation
- Random typo generation at a configurable error rate
- Automatic backspace-and-correct behavior
- Mimics real human mistake patterns

### Typing Sound Packs
| Pack | Description |
|---|---|
| Mechanical | Classic mechanical keyboard clicks |
| Soft | Quiet laptop-style keypresses |
| Fast | Rapid typist sound effects |
| Normal | Standard click sounds |
| Gaming | Dynamic gaming keyboard style |

### UI Themes
| Theme | Style |
|---|---|
| Dark | Clean dark background |
| Neon | Vivid neon accent colors |
| Hacker | Green-on-black terminal feel |
| Matrix | Cascading digital aesthetic |
| Minimal | Light, distraction-free layout |

### Live Statistics
Track real-time typing analytics during each session:
- Characters typed, errors, and corrections
- Elapsed duration and average WPM

### Custom Typing Profiles
Save and load named profiles with individual settings for speed, error rate, sounds, and pause behavior.

### Productivity Controls
- Paste from clipboard
- Pause / Resume mid-typing
- Stop at any time
- Live word and character counter

---

## Screenshots

> Add screenshots to the `screenshots/` folder and update the paths below.

```
screenshots/main_ui.png
screenshots/settings_panel.png
screenshots/themes_preview.png
```

---

## Tech Stack

| Technology | Role |
|---|---|
| Python | Core application logic |
| Tkinter | Desktop GUI framework |
| PyAutoGUI | Keyboard automation |
| Pygame | Sound effect playback |
| Threading | Non-blocking background typing |
| JSON | Settings and profile persistence |

---

## Project Structure

```
TypeMimic/
├── assets/
│   └── logo.ico
├── core/
│   ├── controller.py        # Typing session orchestration
│   ├── typing_engine.py     # Core human-like typing logic
│   ├── settings_manager.py  # Load/save settings
│   ├── profiles.py          # Profile management
│   └── path_helper.py       # Cross-platform path resolution
├── data/
│   └── settings.json        # Default settings
├── gui/
│   ├── gui.py               # Main application window
│   └── themes.py            # Theme definitions
├── sounds/
│   ├── mechanical.wav
│   ├── soft_click.wav
│   └── fast_keyboard.wav
├── screenshots/
├── main.py
├── requirements.txt
└── README.md
```

---

## Installation

**Prerequisites:** Python 3.8 or higher

```bash
# 1. Clone the repository
git clone https://github.com/SAJLENDRAPANDEY/TypeMimic_Ai.git
cd TypeMimic_Ai

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
python main.py
```

---

## Build EXE

Package TypeMimic AI as a standalone Windows executable:

```bash
python -m PyInstaller \
  --onefile \
  --windowed \
  --icon=assets/logo.ico \
  --hidden-import pygame \
  --hidden-import pyautogui \
  --add-data "assets;assets" \
  --add-data "sounds;sounds" \
  --add-data "data;data" \
  main.py
```

The compiled `.exe` will appear in the `dist/` folder.

---

## Download

A pre-built Windows executable is available on Google Drive:

**[⬇ Download TypeMimic AI (EXE)](https://drive.google.com/uc?export=download&id=1IhP73dtAm0h_6a6SAzIgaEsAXt0V9jjM)**

---

## Roadmap

- [ ] AI-powered typing prediction
- [ ] Global hotkey support
- [ ] Typing macros and sequences
- [ ] Multi-language support
- [ ] Custom sound import
- [ ] Advanced analytics dashboard
- [ ] Auto-save sessions
- [ ] Cloud sync for profiles
- [ ] Productivity tool integrations

---

## Contributing

Contributions are welcome. To get started:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add your feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

Please open an issue first for major changes so we can discuss the approach.

---

## License

This project is released for educational and productivity purposes. See [LICENSE](LICENSE) for details.

---

## Author

**Sajlendra Pandey**

[![GitHub](https://img.shields.io/badge/GitHub-SAJLENDRAPANDEY-181717?style=flat-square&logo=github)](https://github.com/SAJLENDRAPANDEY)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-sajlendra--pandey-0A66C2?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/sajlendra-pandey-37378627b/)
[![Portfolio](https://img.shields.io/badge/Portfolio-sajlendrapandey.netlify.app-00C7B7?style=flat-square&logo=netlify)](https://sajlendrapandey.netlify.app/)

---

<div align="center">

If TypeMimic AI is useful to you, consider leaving a ⭐ — it helps others discover the project.

</div>
