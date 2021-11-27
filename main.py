from flask.wrappers import Request
from superres.superres import videoStream


def superres(request: Request):
    # print("received request!")
    # print(request.headers)
    video = request.files["video"]
    if video is None:
        return "No video sent!"
    videoStream(video)
    return f"Received {len(request.files)} files ."
