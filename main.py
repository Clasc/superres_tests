from flask.wrappers import Request
from superres import supperresVideo, videoStream


def hello_world(request: Request):
    return "<h1>Hello, World!</h1>"


def superres(request: Request):
    # print(request.headers)
    video = request.files["video"]
    if video is None:
        return "No video sent!"
    videoStream(video)
    return f"Received {len(request.files)} files ."
