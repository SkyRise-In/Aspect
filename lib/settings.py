import json


class Settings(object):
    def __init__(self):
        # Get the user config settings.
        with open("settings.json", "r") as f:
            data = json.load(f)
            self.username = data["username"]
            self.bot_name = data["name"]
            self.gender = data["gender"]
