import os
import os.path

from flask import (
    Flask,
    render_template,
)

app = Flask(__name__)
app.config.from_object("config")
motion_directory = os.path.abspath(app.config["MOTION_DIRECTORY"])

if not os.path.isdir(motion_directory):
    raise Exception(f"Not a folder: {motion_directory}")

@app.route("/")
def index():
    files = [path for path in [os.path.join(motion_directory, name) for name in os.listdir(motion_directory)] if os.path.isfile(path)]
    days = [{"files": files}, {"files": files}]
    return render_template("index.html", days=days)

@app.route("/delete", methods=["POST"])
def delete():
    return "Not implemented"

if __name__ == "__main__":
    app.run()
