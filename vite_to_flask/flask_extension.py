import typing as t
from pathlib import Path

from flask import Flask, url_for, send_from_directory
from markupsafe import Markup

from ._html_tags import BodyContent, ScriptTag, LinkTag
from .helpers import Colr


class ViteToFlask:
    app: t.Optional[Flask]
    vtf_root_path: Path

    def __init__(self, app: t.Optional[Flask] = None) -> None:
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        if app is None:
            raise ImportError("No app was passed in.")
        if not isinstance(app, Flask):
            raise TypeError("The app that was passed in is not an instance of Flask")

        self.app = app

        if "vite_to_flask" in self.app.extensions:
            raise ImportError(
                "The app has already been initialized with vite-to-flask."
            )

        self.app.extensions["vite_to_flask"] = self
        self.app.config["VTF_APPS"] = {}
        self.vtf_root_path = Path(app.root_path) / "vtf"

        if not self.vtf_root_path.exists():
            raise FileNotFoundError(
                "vtf directory not found in the flask app root directory."
            )

        for folder in self.vtf_root_path.iterdir():
            if folder.is_dir():
                self.app.config["VTF_APPS"].update({folder.name: folder})

        self._load_routes(app)
        self._load_context_processor(app)
        self._load_cors_headers(app)

    def _load_routes(self, app: Flask) -> None:
        @app.route("/__vtf/<vite_app>/<filename>")
        def __vtf(vite_app: str, filename: str):
            return send_from_directory(self.vtf_root_path / vite_app, filename)

    @staticmethod
    def _load_context_processor(app: Flask) -> None:
        @app.context_processor
        def vtf_head_processor():
            def vtf_head(vite_app: str) -> t.Any:
                vite_assets = Path(app.root_path) / "vtf" / vite_app
                find_vite_js = vite_assets.glob("*.js")
                find_vite_css = vite_assets.glob("*.css")

                tags = []

                for file in find_vite_js:
                    tags.append(
                        ScriptTag(
                            src=url_for(
                                "__vtf", vite_app=f"{vite_app}", filename=f"{file.name}"
                            ),
                            type_="module",
                        )
                    )

                for file in find_vite_css:
                    tags.append(
                        LinkTag(
                            rel="stylesheet",
                            href=url_for(
                                "__vtf", vite_app=f"{vite_app}", filename=f"{file.name}"
                            ),
                        )
                    )

                return Markup("".join([tag.raw() for tag in tags]))

            return dict(vtf_head=vtf_head)

        @app.context_processor
        def vtf_body_processor():
            def vtf_body(
                root_id: str = "root",
                noscript_message: str = "You need to enable JavaScript to run this app.",
            ) -> t.Any:
                return BodyContent(root_id, noscript_message)()

            return dict(vtf_body=vtf_body)

    @staticmethod
    def _load_cors_headers(app: Flask) -> None:
        if app.debug and not app.config.get("VTF_DISABLE_DEBUG_CORS", False):
            print(
                f"{Colr.OKCYAN}{Colr.BOLD}vite-to-flask: Flask debug mode detected"
                f"{Colr.END}{Colr.END}\n\r"
                f"{Colr.OKCYAN}Allow all CORS headers will be added to "
                f"every response to allow for frontend development.{Colr.END}"
            )

            @app.after_request
            def after_request(response):
                response.headers["Access-Control-Allow-Origin"] = "*"
                response.headers["Access-Control-Allow-Headers"] = "*"
                response.headers["Access-Control-Allow-Methods"] = "*"
                return response
