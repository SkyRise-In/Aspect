from random import choice
import speech_recognition as sr
from os import get_terminal_size
from os import system, name
import json
import pyttsx3

# Initialize the voice engine.
engine = pyttsx3.init()
voices = engine.getProperty("voices")

# Init the speech recognition.
r = sr.Recognizer()

# Get the user config settings.
with open("settings.json", "r") as f:
    data = json.load(f)
    username = data["username"]
    bot_name = data["name"]
    voice = data["gender"]

# Add support for voices in Linux and windows.
if name == "posix":
    if voice == "male":
        engine.setProperty("voice", "english")

    elif voice == "female":
        engine.setProperty("voice", "english_rp+f3")

elif name == "nt":
    if voice == "male":
        engine.setProperty("voice", voices[0].id)

    elif voice == "female":
        engine.setProperty("voice", voices[1].id)


class Colors:
    red = "\033[31m"
    blue = "\033[34m"
    green = "\033[32m"
    purple = "\033[35m"
    brown = "\033[33m"
    yellow = "\033[1;33m"
    cyan = "\033[36m"
    pink = "\033[35;1m"
    reset = "\033[0m"


class Assistant:
    """A class to reperesent an Assistant."""

    def __init__(self, username, bot_name):
        # Chars to remove from the user_input.
        self.bad_chars = [",", "!", "?", "."]
        self.messages = []
        self.username = username
        self.bot_name = bot_name

        self.terminal_size = get_terminal_size()

    def run(self):
        """A function to run the Assistant."""
        print("Hit ^C or type 'quit' or 'exit' to exit.")
        while True:
            self.terminal_size = get_terminal_size()

            # If the user tries to hit ^C then quit the program.
            try:
                if len(self.messages) >= self.terminal_size[1]:
                    self._clear()

                    # Find out how many lines are available.
                    i = self.terminal_size[1] - 2

                    # Start from point i when printing the list.
                    j = len(self.messages) - i

                    for message in self.messages[j:]:
                        print(message)

                else:

                    # print("\n" * (37 - len(self.messages)))
                    self._clear()

                    for message in self.messages:
                        print(message)

                    print("\n" * ((self.terminal_size[1] - len(self.messages)) - 3))

                user_input = self._prompt()
            except KeyboardInterrupt:
                exit()

            user_input = self._clean(user_input)
            self.messages.append(
                f"{Colors.red}{username}{Colors.reset}:{Colors.purple} {user_input}{Colors.reset}"
            )
            response = self._bag(user_input)

            # If the intent is not return then it means that JARVIS cannot understand the user.
            if response is None:
                with open("src/log.txt", "a") as f:
                    f.write(f"\n{user_input}\n")
                continue

            # Check if there is a return value from the bag function.
            if user_input:
                output = self._respond(response)

                self.messages.append(self._format_string(output))
                engine.say(self._clean(output))
                engine.runAndWait()

    def _prompt(self):
        print("=" * self.terminal_size[0])
        # command = input(f"{Colors.red}You{Colors.reset}:{Colors.purple} ")

        try:
            with sr.Microphone() as source:
                # r.adjust_for_ambient_noise(source, duration=0.2)
                audio = r.listen(source)

                text = r.recognize_google(audio)
                text = text.lower()
                command = text

        except Exception:
            command = ""

        return command

    def _clean(self, string):
        """A function to clean the user input"""
        string = str(string)
        string = string.lower()
        string = string.strip()

        for char in self.bad_chars:
            string = string.replace(char, "")

        if string == "exit":
            exit()
        elif string == "quit":
            exit()

        return string

    def _bag(self, string):
        with open("src/data.json", "r") as f:
            data = json.load(f)

        for intent in data["intents"]:
            doc_x = []
            user_input = string.split(" ")
            output = []
            index = 0
            match = 0

            for pattern in intent["patterns"]:
                pattern = pattern.split(" ")

                for word in pattern:
                    doc_x.append(word)

            for word in user_input:
                output.append(0)
                for word_x in doc_x:
                    if word == word_x:
                        output[index] = 1
                        # NOTE: This breaks out of the current loop and goes into the first loop.
                        break

                    else:
                        # If the word does not match then make the current index `0`.
                        output[index] = 0

                index += 1

            # Checking loop. This loop checks to see how many times the words match.
            for number in output:
                if number != 0:
                    match += 1

            if match >= (len(output) / 2):
                return intent

    def _format_string(self, string):
        return f"{Colors.reset}{Colors.green}{self.bot_name}{Colors.reset}: {Colors.blue}{string}{Colors.reset}"

    def _respond(self, intent):
        return choice(intent["responses"])

    def _clear(self):
        """A function to clear the terminal screen"""
        if name == "nt":
            system("cls")

        else:
            system("clear")


if __name__ == "__main__":
    assistant = Assistant(username, bot_name)
    assistant.run()
