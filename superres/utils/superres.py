import os
import tempfile
import base64
import cv2
from cv2 import FileStorage
from werkzeug.utils import secure_filename

from utils.publish import Publisher

publisher = Publisher()
publisher.initialize(publisher._topics[0])


def vidToFrames(filepath: str) -> list:
    capture = cv2.VideoCapture(filepath)
    frames = []
    while capture.isOpened():
        ret, frame = capture.read()
        if ret == False:
            break
        frames.append(frame)
    capture.release()
    return frames


def publishVidFrames(video: FileStorage) -> int:
    tempfilepath = get_file_path(video.filename)
    video.save(tempfilepath)
    frames = vidToFrames(tempfilepath)
    os.remove(tempfilepath)
    for frame in frames:
        data = encodeImage(frame)
        publisher.publish("frame", data)
    return len(frames)


def encodeImage(img: Any, extension=".jpg") -> str:
    retval, buffer = cv2.imencode(extension, img)
    if buffer is None:
        print("error encoding image, buffer is empty")
        return ""
    return base64.b64encode(buffer)


def get_file_path(filename):
    # Note: tempfile.gettempdir() points to an in-memory file system
    # on GCF. Thus, any files in it must fit in the instance's memory.
    file_name = secure_filename(filename)
    return os.path.join(tempfile.gettempdir(), file_name)


# superresImage("images/oma.jpg")
# time = measure(lambda: supperresVideo("images/rotating-boy.gif", "out/vid/video.avi"))

# print("superresing video took: ", time)
