import os
import os.path

from flask import (
    Flask,
    render_template,
    send_from_directory,
)

app = Flask(__name__)
app.config.from_object("config")
motion_directory = os.path.abspath(app.config["MOTION_DIRECTORY"])

if not os.path.isdir(motion_directory):
    raise Exception(f"Not a folder: {motion_directory}")

@app.route("/")
def index():
    files = [f for f in os.listdir(motion_directory) if os.path.isfile(os.path.join(motion_directory, f))]
    days = [{"files": files}, {"files": files}]
    return render_template("index.html", days=days)

@app.route("/delete", methods=["POST"])
def delete():
    return "Not implemented"

@app.route("/file/<name>")
def file(name):
    return send_from_directory(motion_directory, name)

if __name__ == "__main__":
    app.run()
