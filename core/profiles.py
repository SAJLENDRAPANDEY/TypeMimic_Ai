PROFILES = {

    "Human Slow": {

    "min_delay": 0.08,
    "max_delay": 0.16,

    "error_rate": 0.03,

    "thinking_pause": (0.4, 1.0),

    "sound": "sounds/soft_click.wav",

    "volume": 0.6
    },
    "Student": {

        "min_delay": 0.07,
        "max_delay": 0.16,

        "error_rate": 0.05,

        "thinking_pause": (0.6, 1.5),

        "sound": "sounds/normal_click.wav"
    },

    "Programmer": {

        "min_delay": 0.04,
        "max_delay": 0.09,

        "error_rate": 0.01,

        "thinking_pause": (0.2, 0.5),

        "sound": "sounds/mech_keyboard.wav"
    },

    "Fast Typist": {

        "min_delay": 0.02,
        "max_delay": 0.05,

        "error_rate": 0.01,

        "thinking_pause": (0.2, 0.5),

        "sound": "sounds/fast_keyboard.wav"
    },

    "Mechanical Keyboard": {

        "min_delay": 0.05,
        "max_delay": 0.11,

        "error_rate": 0.03,

        "thinking_pause": (0.4, 0.9),

        "sound": "sounds/mechanical.wav"
    },

    "Careless Typist": {

        "min_delay": 0.06,
        "max_delay": 0.15,

        "error_rate": 0.10,

        "thinking_pause": (0.3, 1.0),

        "sound": "sounds/normal_click.wav"
    }
}

from core.settings_manager import load_settings

settings = load_settings()

custom_profiles = settings.get(
    "custom_profiles",
    {}
)

PROFILES.update(custom_profiles)