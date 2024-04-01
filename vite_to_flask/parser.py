import argparse

from vite_to_flask.helpers import Colr


class ArgumentParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        super(ArgumentParser, self).__init__(*args, **kwargs)
        self.vite_apps: list[dict] = []

    def print_help(self, file=None):
        print(
            "\n\r"
            "Usage: vtf <command>"
            "\n\r\n\r"
            f" {Colr.BOLD}compile{Colr.END} => Attempt to compile all vite apps"
            "\n\r"
            f" {Colr.BOLD}list{Colr.END} => List all vite apps in pyproject.toml"
            "\n\r"
            f" {Colr.BOLD}-h, --help{Colr.END} => Show the help message and exit"
            "\n\r"
            f" {Colr.BOLD}-v, --version{Colr.END} => Show the version and exit"
        )
        print("")
