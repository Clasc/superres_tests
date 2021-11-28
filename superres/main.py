from flask.wrappers import Request
from utils.superres import convertAndUpresVid


def superres(request: Request):
    video = request.files["video"]
    if video is None:
        return "No video sent!"
    framesupresd = convertAndUpresVid(video)
    return f"Received {framesupresd} files ."
