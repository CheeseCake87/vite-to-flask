# 🚛 vite-to-flask

**Transport Vite apps to Flask.**

```bash
pip install vite-to-flask
```

## How it works

### The pyproject.toml file

The pyproject.toml file is used to store what Vite apps are available.

Adding the following to the pyproject.toml file will transfer all the Vite
apps listed in the `vite_app_dirs` list to the Flask app listed in the `flask_app_dir` key.

`pyproject.toml`:

```toml
[tool.vtf]
npx_exec = "npx"
flask_app_dir = "app_flask_demo"
vite_app_dirs = ["app_vite_demo"]
```

The compiling of the Vite apps requires the `npx` command to be
available. You can use absolute paths to npx here.

### List the Vite apps

You can see what apps can be compiled by running:

```bash
vtf list
```

### Compiling the Vite apps

```bash
vtf compile
```

The Vite apps are compiled into a `dist` folder, the files contained
in this folder is then moved to a folder called `vtf` in the Flask app.

Any js file that is compiled that contains an asset reference will
replace `assets/` with `/__vtf/{app_name}`.

## Working with vite-to-flask

vite-to-flask creates a couple of Flask context processors that match the Vite apps
to a Flask template.

It also creates a Flask route that serves the Vite app files.

### The context processors

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    {{ vtf_head('app_vite_demo') }}
    <title>Test</title>
</head>
<body>
{{ vtf_body() }}
</body>
</html>
```

```
vtf_head(
    vite_app_name: str
)
```

```
vtf_body(
    root_id: str = "root",
    noscript_message: str = "You need to enable JavaScript to run this app.",
)
```

### The route

```python
@app.route("/__vtf/<vite_app>/<filename>")
def __vtf(vite_app: str, filename: str):
    return send_from_directory(vtf_dir / vite_app, filename)
```

## CORS

vite-to-flask will add the following CORS headers to the Flask app, only in debug mode:

```python
if app.debug and not app.config.get('VTF_DISABLE_DEBUG_CORS', False):
    @app.after_request
    def add_cors_headers(response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "*"
        return response
```

This is to allow the Vite app to communicate with the Flask app during development.

As you can probably work out, you can disable this behavior by setting a Flask config value
of `VTF_DISABLE_DEBUG_CORS` to `True`

## Running the example

```bash
pip install vite-to-flask
```

```bash
cd app_vite_demo
```

```bash
npm i
```

```bash
cd ..
```

```bash
vtf compile
```

```bash
flask --app app_flask_demo run --debug
```