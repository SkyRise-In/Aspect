# Native Python Imports
import json
from os import system, name

# Custom Imports
from installer.settings import Settings
from installer.log import Log
from installer.py_command import py_venv_command


log = Log()
log.info("Starting install script.")
log.info("Setting up user settings file.")

username = log.input(
    "Hi there, in order to get you set up we are going to need a username from you.\nWhat would you like that to be?"
)
log.succeed(f"Username set to `{username}`.")

bot_name = log.input("Great, now what do you want to call me?")
log.succeed(f"Bot name set to `{bot_name}`.")

gender = log.choice("What voice should I use?", ["male", "female"])
log.succeed(f"Voice set to `{gender}`.")

settings = {"username": username, "name": bot_name, "gender": gender}
file = open("settings.json", "w")
json.dump(settings, file, indent=2)

log.info("Installing python packages.")
system("python3 -m venv env")

py_venv_command(f"-m pip install -r {Settings.requirements_file}")
py_venv_command("main.py")

log.succeed("Great, now just run `main.py` in order to chat!")
