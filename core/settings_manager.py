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

import json

SETTINGS_FILE = "data/settings.json"


def load_settings():

    with open(
        SETTINGS_FILE,
        "r"
    ) as file:

        return json.load(file)


def save_settings(settings):

    with open(
        SETTINGS_FILE,
        "w"
    ) as file:

        json.dump(
            settings,
            file,
            indent=4
        )


def save_custom_profile(
    profile_name,
    profile_data
):

    settings = load_settings()

    settings["custom_profiles"][profile_name] = profile_data

    save_settings(settings)

def delete_custom_profile(profile_name):

    settings = load_settings()

    if profile_name in settings["custom_profiles"]:

        del settings["custom_profiles"][profile_name]

        save_settings(settings)


def update_custom_profile(
    profile_name,
    profile_data
):

    settings = load_settings()

    settings["custom_profiles"][profile_name] = profile_data

    save_settings(settings)