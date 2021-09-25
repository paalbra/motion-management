import os
import os.path
import re

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
    paths = [f for f in os.listdir(motion_directory) if os.path.isfile(os.path.join(motion_directory, f))]
    days = {}
    for path in paths:
        match = re.match(r"^(?P<date>\d{8})_(?P<time>\d{6})-(?P<event>\d+)\.png$", path)
        if match:
            date = match.group("date")
            if date not in days:
                days[date] = {"files": [path]}
            else:
                days[date]["files"].append(path)
    return render_template("index.html", days=days.values())

@app.route("/delete", methods=["POST"])
def delete():
    return "Not implemented"

@app.route("/file/<name>")
def file(name):
    return send_from_directory(motion_directory, name)

if __name__ == "__main__":
    app.run()
