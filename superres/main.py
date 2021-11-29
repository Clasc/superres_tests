from flask.wrappers import Request
from utils.superres import publishVidFrames


def superres(request: Request):
    video = request.files["video"]
    if video is None:
        return "No video sent!"
    frames = publishVidFrames(video)
    return f"Published {frames} files ."
