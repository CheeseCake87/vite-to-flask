import argparse

from vite_to_flask.helpers import Colr


class ArgumentParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        super(ArgumentParser, self).__init__(*args, **kwargs)
        self.vite_apps: list[dict] = []

    def print_help(self, file=None):
        print(
            "\n\r"
            "Usage: vtf <option>"
            "\n\r\n\r"
            f" {Colr.OKCYAN}list{Colr.END} => List all vite apps in pyproject.toml"
            "\n\r"
            f" {Colr.OKCYAN}compile (-y){Colr.END} => Attempt to compile all vite apps"
            "\n\r"
            f"  | {Colr.OKCYAN}-y{Colr.END} => Accept all prompts while compiling"
            "\n\r"
            f" {Colr.OKCYAN}-h, --help{Colr.END} => Show the help message and exit"
            "\n\r"
            f" {Colr.OKCYAN}-v, --version{Colr.END} => Show the version and exit"
        )
        print("")
