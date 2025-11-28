# motion-management

## About

Simple [Flask](https://flask.palletsprojects.com/) app for managing [Motion](https://motion-project.github.io/) events (pictures and movies).

## Quick start

```
cp config.sample.py config.py
python3 -m venv venv
. venv/bin/activate
pip install flask
FLASK_APP=app.py FLASK_ENV=development flask run
```

## Howto

Want to convert video first:

```
for v in $(ls ./motion-sample/*.avi); do ffmpeg -i $v -vcodec h264 ${v//.avi}.mp4; done
```
