import json

# install.py by Hudson Smith.


# Create the log object that will be used for logging info.
class Log(object):
    """Log object that can be used to log pretty printed info to the terminal window."""

    def __init__(self) -> None:
        """Make global colors."""
        self.reset: str = "\033[0m"
        self.bold: str = "\033[1m"
        self.italic: str = "\033[3m"
        self.underline: str = "\033[4m"
        self.blinking: str = "\033[5m"
        self.reverse: str = "\033[7m"
        self.black: str = "\033[30m"
        self.red: str = "\033[31m"
        self.green: str = "\033[32m"
        self.brown: str = "\033[33m"
        self.blue: str = "\033[34m"
        self.purple: str = "\033[35m"
        self.cyan: str = "\033[36m"
        self.grey: str = "\033[37m"
        self.yellow: str = "\033[1;33m"

    def fail(self, string: str) -> None:
        print(
            f"{self.red}{self.bold}[x]{self.reset} {self.red}{self.italic}{string}{self.reset}"
        )

    def info(self, string: str) -> None:
        print(
            f"{self.blue}{self.bold}[i]{self.reset} {self.blue}{self.italic}{string}{self.reset}"
        )

    def warn(self, string: str) -> None:
        print(
            f"{self.yellow}{self.bold}[!]{self.reset} {self.yellow}{self.italic}{string}{self.reset}"
        )

    def succeed(self, string: str) -> None:
        print(
            f"{self.green}{self.bold}[*]{self.reset} {self.green}{self.italic}{string}{self.reset}"
        )

    def input(self, string: str) -> str:
        # Make new line formatting a little nicer.
        string: str = string.replace("\n", "\n    ")

        # Get the user input.
        value: str = str(
            input(
                f"{self.cyan}{self.bold}[>]{self.reset} {self.cyan}{self.italic}{string} > {self.underline}{self.italic}{self.purple}"
            )
        )

        # Clear the custom coloring.
        print(self.reset, end="")
        return value

    def choice(self, string: str, choices: list) -> str:
        # Make new line formatting a little nicer.
        string = string.replace("\n", "\n    ")

        for i, choice in enumerate(choices, start=1):
            print(
                f"    {self.bold}{self.cyan}[{i}]{self.reset} {self.cyan}{self.italic}{choice}{self.reset}"
            )

        while True:
            try:
                # Subtract by one to get 0 indexed array number.
                value: int = (
                    int(
                        input(
                            f"{self.cyan}{self.bold}[>]{self.reset} {self.cyan}{self.italic}{string} > {self.underline}{self.italic}{self.purple}"
                        )
                    )
                    - 1
                )

                print(end=f"{self.reset}")
                return choices[value]

            except ValueError:
                print(end=f"{self.reset}")
                self.warn(f"Enter an integer from 1 to {len(choices)}.")


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

log.succeed("Great, now just run `main.py` in order to chat!")
