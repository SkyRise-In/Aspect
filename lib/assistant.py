from lib.colors import Colors
from lib.clear import clear

import speech_recognition as sr

from os import get_terminal_size
import json

from random import choice

# For typing purposes
from pyttsx3 import Engine


class Assistant(object):
    """A class to reperesent an Assistant."""

    def __init__(self, username, bot_name, engine: Engine | None):
        # Chars to remove from the user_input.
        self.bad_chars = [",", "!", "?", "."]
        self.messages = []
        self.username = username
        self.bot_name = bot_name

        self.terminal_size = get_terminal_size()
        self.engine = engine
        self.on = False

    def run(self) -> None:
        pass

    def draw_console(self):
        """A function to run the Assistant."""
        print("Hit ^C or type 'quit' or 'exit' to exit.")
        self.terminal_size = get_terminal_size()

        # If the user tries to hit ^C then quit the program.
        # try:
        if len(self.messages) >= self.terminal_size[1]:
            clear()

            # Find out how many lines are available.
            i = self.terminal_size[1] - 2

            # Start from point i when printing the list.
            j = len(self.messages) - i

            for message in self.messages[j:]:
                print(message)

        else:
            clear()

            for message in self.messages:
                print(message)

            print("\n" * ((self.terminal_size[1] - len(self.messages)) - 3))

            user_input = self._prompt()

            if self._clean(user_input) == f"hey {self.bot_name}":
                self.on = True
            
            else:
                self.on = False

        # except KeyboardInterrupt:
        #     exit()

        # user_input = self._clean(user_input)
        # self.messages.append(
        #     f"{Colors.red}{self.username}{Colors.reset}:{Colors.purple} {user_input}{Colors.reset}"
        # )
        # response = self._bag(user_input)

        # If the intent is not return then it means that JARVIS cannot understand the user.
        if response is None:
            with open("src/log.txt", "a") as f:
                f.write(f"\n{user_input}\n")

        # Check if there is a return value from the bag function.
        if user_input:
            output = self._respond(response)

            # Add the formatted string to the output.
            #
            # Like the equivalent of printing, except that the text
            # is drawn the next iteration of the loop
            self.messages.append(self._format_string(output))

            if self.engine:
                self.engine.say(self._clean(output))
                self.engine.runAndWait()

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
            command = input("YOU: ").replace("YOU: ", "")

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
