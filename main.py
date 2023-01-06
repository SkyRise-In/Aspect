from lib.voices import return_voice
from lib.settings import Settings
from lib.assistant import Assistant

# Init settings to read json data.
settings: Settings = Settings()

if __name__ == "__main__":
    assistant = Assistant(settings.username, settings.bot_name, return_voice(settings.gender))
    assistant.run()
