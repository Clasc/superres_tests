from flask import Flask, request
from superres import supperresVideo, videoStream

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<h1>Hello, World!</h1>"


@app.route("/superrestest")
def superrestest():
    input = request.args.get("in")
    out = request.args.get("out")
    print(input, out)
    if input is None or out is None:
        return "error, missing arguments"
    supperresVideo(input, out)
    return "Done!"


@app.route("/superres", methods=["POST"])
def superres():
    # print(request.headers)
    video = request.files["video"]
    if video is None:
        return "No video sent!"
    videoStream(video)
    return f"Received {len(request.files)} files ."
