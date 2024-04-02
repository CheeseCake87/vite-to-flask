from flask import Flask

from app_flask_demo.extensions import vite_to_flask


def setup_blueprints(app):
    from app_flask_demo.www import bp

    app.register_blueprint(bp)


def create_app():
    app = Flask(__name__)

    # app.config["VTF_DISABLE_DEBUG_CORS"] = True

    vite_to_flask.init_app(app)

    setup_blueprints(app)

    return app
