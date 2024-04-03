import shlex
import shutil
import subprocess
import sys
from pathlib import Path
from tomllib import loads


class Colr:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


class PyProjectConfig:
    cwd: Path
    pyproject: Path
    vtf_config: dict

    npx_exec: str
    flask_app_dir: str
    flask_static_root: Path
    vite_apps: list

    def __init__(self):
        self.cwd = Path.cwd()
        self.pyproject = self.cwd / "pyproject.toml"
        self.load_pyproject()

    def load_pyproject(self):
        if not self.pyproject.exists():
            raise FileNotFoundError("pyproject.toml not found.")

        pyproject_raw = loads(str(self.pyproject.read_text()))
        self.vtf_config = pyproject_raw.get("tool", {}).get("vtf", {})
        self.npx_exec = self.vtf_config.get("npx_exec", "npx")
        self.flask_app_dir = self.vtf_config.get("flask_app_dir", "app")
        self.vite_apps = self.vtf_config.get("vite_app_dirs", [])

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return None


class VTFConfig:
    vtf_path: Path
    vtf_config: dict

    def __init__(self, app_path: Path):
        self.vtf_path = app_path / "vtf"
        self.vtf_config_path = self.vtf_path / "config.toml"
        self.load_pyproject()

    def load_pyproject(self):
        if not self.vtf_config_path.exists():
            raise FileNotFoundError("vtf/config.toml not found.")

        self.vtf_config = loads(str(self.vtf_config_path.read_text()))

    def __enter__(self):
        return self.vtf_config

    def __exit__(self, exc_type, exc_val, exc_tb):
        return None


class NPXCommander:
    def __init__(self, workdir: Path, npx_binary: str = "npx"):
        self.npx_binary = npx_binary
        self.workdir = workdir

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return None

    def run(self, command: str):
        subprocess.run([self.npx_binary, *shlex.split(command)], cwd=self.workdir)
        pass


def _compile(pypro: PyProjectConfig, vite_apps: list[dict], replace: bool = False):
    print("Compiling Vite apps...")
    flask_vtf_dir = pypro.cwd / pypro.flask_app_dir / "vtf"

    # Delete contents of vtf_dir
    if flask_vtf_dir.exists():
        if not replace:
            prompt = input(
                f"Continuing will replace the contents of \n\r"
                f"{flask_vtf_dir} \n\r"
                f"Do you want to continue? (Y/n): "
            )
        else:
            prompt = "y"

        if prompt.lower() == "y" or prompt == "":
            for item in flask_vtf_dir.iterdir():
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()

        else:
            print("Operation aborted.")
            sys.exit(0)

    else:
        flask_vtf_dir.mkdir()

    # Create directories for vite apps
    for app in vite_apps:
        flask_vtf_app_dir = flask_vtf_dir / app.get("vite_app")
        this_vite_app_path = pypro.cwd / app.get("vite_app")
        this_vite_app_dist = this_vite_app_path / "dist"
        this_vite_app_dist_assets = this_vite_app_dist / "assets"
        this_vite_flask_path = flask_vtf_dir / app.get("vite_app")

        if not flask_vtf_app_dir.exists():
            flask_vtf_app_dir.mkdir()

        with NPXCommander(this_vite_app_path, pypro.npx_exec) as npx:
            npx.run("vite build --mode production")

        for item in this_vite_app_dist_assets.iterdir():
            print(f"Copying {item.name} to {this_vite_flask_path}")

            if item.suffix == ".js":
                with open(this_vite_flask_path / item.name, "w") as f:
                    content = item.read_text()
                    f.write(content.replace("assets/", f"__vtf/{app.get('vite_app')}/"))
            else:
                shutil.copy(item, this_vite_flask_path / item.name)

        shutil.rmtree(this_vite_app_dist)

    print("Compilation complete.")
