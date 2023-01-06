from os import system, name


def clear():
    """A function to clear the terminal screen"""
    if name == "nt":
        system("cls")

    else:
        system("clear")
