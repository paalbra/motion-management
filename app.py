import datetime
import glob
import os
import os.path
import re

from flask import (
    Flask,
    render_template,
    request,
    send_from_directory,
)



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
        if match := re.match(app.config["IMAGE_FILE_PATTERN"], path):
            image_path = path
            video_path = ".".join(image_path.split(".")[:-1] + [app.config["VIDEO_EXTENSION"]])
            fileref = os.path.splitext(path)[0]
            timestamp = datetime.datetime.strptime(match.group("date") + match.group("time"), app.config["DATE_FORMAT"] + app.config["TIME_FORMAT"])
            date = timestamp.date()

            file_object = {
                "fileref": fileref,
                "image_path": image_path,
                "video_path": video_path,
            }
            if date not in days:
                days[date] = [file_object]
            else:
                days[date].append(file_object)

    return render_template("index.html", days=days)

@app.route("/delete", methods=["POST"])
def delete():
    if request.is_json:
        data = request.json
        if "fileref" in data:
            glob_filter = os.path.join(motion_directory, f"{data['fileref']}.*")
            files = glob.glob(glob_filter)
            for _file in files:
                os.remove(_file)
            return data["fileref"]

    return "Bad data", 400

@app.route("/file/<name>")
def file(name):
    return send_from_directory(motion_directory, name)

if __name__ == "__main__":
    app.run()
