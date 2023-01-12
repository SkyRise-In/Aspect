from typing import Union
import speech_recognition as sr
from os import name
import pyttsx3

# For typing purposes.
from pyttsx3 import Engine


def return_voice(gender=Union["male", "female"]) -> Engine | None:
    engine = None

    try:
        engine = pyttsx3.init()
        voices = engine.getProperty("voices")

        # Init the speech recognition.
        r = sr.Recognizer()

        # Add support for voices in Linux and windows.
        if name == "posix":
            if gender == "male":
                engine.setProperty("voice", "english")

            elif gender == "female":
                engine.setProperty("voice", "english_rp+f3")

        elif name == "nt":
            if gender == "male":
                engine.setProperty("voice", voices[0].id)

            elif gender == "female":
                engine.setProperty("voice", voices[1].id)

    except OSError:
        print("Audio source not found, falling back to text-only.")

    return engine
