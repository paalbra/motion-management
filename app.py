import datetime
import os
import os.path
import re

from flask import (
    Flask,
    render_template,
    send_from_directory,
)

IMAGE_FILE_PATTERN = r"^(?P<date>\d{8})_(?P<time>\d{6})-(?P<event>\d+)\.png$"
DATE_FORMAT = r"%Y%m%d"
TIME_FORMAT = r"%H%M%S"

app = Flask(__name__)
app.config.from_object("config")
motion_directory = os.path.abspath(app.config["MOTION_DIRECTORY"])

if not os.path.isdir(motion_directory):
    raise Exception(f"Not a folder: {motion_directory}")

@app.route("/")
def index():
    paths = sorted([f for f in os.listdir(motion_directory) if os.path.isfile(os.path.join(motion_directory, f))])
    days = {}
    for path in paths:
        if match := re.match(IMAGE_FILE_PATTERN, path):
            image_path = path
            fileref = os.path.splitext(path)[0]
            timestamp = datetime.datetime.strptime(match.group("date") + match.group("time"), DATE_FORMAT + TIME_FORMAT)
            date = timestamp.date()

            file_object = {
                "fileref": fileref,
                "image_path": image_path,
            }
            if date not in days:
                days[date] = [file_object]
            else:
                days[date].append(file_object)

    return render_template("index.html", days=days)

@app.route("/delete", methods=["POST"])
def delete():
    return "Not implemented"

@app.route("/file/<name>")
def file(name):
    return send_from_directory(motion_directory, name)

if __name__ == "__main__":
    app.run()
