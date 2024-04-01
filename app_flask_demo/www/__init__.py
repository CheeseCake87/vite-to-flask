from flask import Blueprint, render_template

bp = Blueprint("frontend", __name__, url_prefix="/", template_folder="templates")


@bp.route("/")
def index():
    return render_template("www/index.html")
