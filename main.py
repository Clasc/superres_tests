from flask import Flask, request
from superres import supperresVideo, videoStream

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<h1>Hello, World!</h1>"


@app.route("/superres", methods=["POST"])
def superres():
    # print(request.headers)
    video = request.files["video"]
    if video is None:
        return "No video sent!"
    videoStream(video)
    return f"Received {len(request.files)} files ."
