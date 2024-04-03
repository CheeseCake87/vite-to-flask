import sys

from .flask_extension import ViteToFlask
from .helpers import PyProjectConfig, _compile, Colr
from .parser import ArgumentParser

__version__ = "0.7.0"
__all__ = ["ViteToFlask"]


def _cli():
    pars = ArgumentParser(prog="vtf", add_help=False)
    pars.add_argument(
        "--version", "-v", action="version", version=f"vite-to-flask {__version__}"
    )
    pars.add_argument("--help", "-h", action="help")

    subparsers = pars.add_subparsers()

    compile_parser = subparsers.add_parser("compile")
    compile_parser.set_defaults(compile=False)
    compile_parser.add_argument("-y", action="store_true")

    list_parser = subparsers.add_parser("list")
    list_parser.set_defaults(list=False)

    ls_parser = subparsers.add_parser("ls")
    ls_parser.set_defaults(list=False)

    with PyProjectConfig() as pyproject:
        for vite_app in pyproject.vite_apps:
            pars.vite_apps.append(
                {
                    "vite_app": vite_app,
                    "flask_app_dir": pyproject.vtf_config.get("flask_app_dir"),
                }
            )

        args = pars.parse_args()

        if hasattr(args, "compile"):
            _compile(
                pyproject,
                pars.vite_apps,
                replace=True if hasattr(args, "y") and args.y else False,
            )

            # exit after compiling
            sys.exit(0)

        if hasattr(args, "list") or hasattr(args, "ls"):
            print("")
            if not pars.vite_apps:
                print(f" {Colr.WARNING}No vite apps found in pyproject.toml{Colr.END}")
            else:
                for app in pars.vite_apps:
                    print(
                        f"{Colr.OKGREEN}{app.get('vite_app')}/dist/assets{Colr.END} "
                        f"{Colr.BOLD}=>{Colr.END} "
                        f"{Colr.OKGREEN}{app.get('flask_app_dir')}/vtf/{app.get('vite_app')}/{Colr.END}"
                    )
            print("")

            # exit after listing
            sys.exit(0)

    # print help if no command is given
    pars.print_help()
