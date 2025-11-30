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
    try:
        filter_value = int(request.args["filter"])
    except:
        filter_value = 7
    filter_date = datetime.datetime.now() - datetime.timedelta(days=filter_value)

    paths = sorted([f for f in os.listdir(motion_directory) if os.path.isfile(os.path.join(motion_directory, f))])
    days = {}
    for path in paths:
        if match := re.match(app.config["IMAGE_FILE_PATTERN"], path):
            image_path = path
            video_path = ".".join(image_path.split(".")[:-1] + [app.config["VIDEO_EXTENSION"]])
            timestamp = datetime.datetime.strptime(match.group("date") + match.group("time"), app.config["DATE_FORMAT"] + app.config["TIME_FORMAT"])
            date = timestamp.date()

            if timestamp < filter_date:
                continue

            file_object = {
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
            file_path = os.path.join(motion_directory, data['fileref'])
            os.remove(file_path)
            return data["fileref"]

    return "Bad data", 400

@app.route("/file/<name>")
def file(name):
    return send_from_directory(motion_directory, name)

if __name__ == "__main__":
    app.run()
