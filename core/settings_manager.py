import json

SETTINGS_FILE = "data/settings.json"


def load_settings():

    with open(SETTINGS_FILE, "r") as file:

        settings = json.load(file)

    return settings


def save_settings(settings):

    with open(SETTINGS_FILE, "w") as file:

        json.dump(
            settings,
            file,
            indent=4
        )