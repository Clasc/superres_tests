import os
import tempfile
import time
import cv2
from cv2 import FileStorage, dnn_superres
from werkzeug.utils import secure_filename

model = lambda: "res/ESPCN_x4.pb"

def create_superSampler():
    sr = cv2.dnn_superres.DnnSuperResImpl_create()
    sr.readModel(model())
    # set the model by passing the value and the upsampling ratio
    sr.setModel("espcn", 4)
    return sr


def upsample(img):
    sr = create_superSampler()
    result = sr.upsample(img)  # upscale the input image
    return result


def superresImage(filepath: str):
    img = cv2.imread(filepath)
    print("image shape:", img.shape)
    result = upsample(img)
    print("endresult:", result.shape)
    cv2.imwrite("out/superrestest.jpg", result)


def measure(func) -> float:
    start = time.time()
    func()
    end = time.time()
    return end - start


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


def upresList(frames: list):
    result = []
    for frame in frames:
        result.append(upsample(frame))
    return result


def writeFrames(frames: list, filename: str):
    if len(frames) <= 0:
        print("frames are empty.")
        return

    height, width, depth = frames[0].shape
    writer = cv2.VideoWriter(
        filename, cv2.VideoWriter_fourcc(*"DIVX"), 15, (width, height)
    )
    for frame in frames:
        writer.write(frame)
    writer.release()


def supperresVideo(input: str) -> list:
    frames = vidToFrames(input)
    return upresList(frames)
    # writeFrames(frames, out)


def convertAndUpresVid(video: FileStorage) -> int:
    tempfilepath = get_file_path(video.filename)
    video.save(tempfilepath)
    frames = supperresVideo(tempfilepath)
    os.remove(tempfilepath)
    return len(frames)


def get_file_path(filename):
    # Note: tempfile.gettempdir() points to an in-memory file system
    # on GCF. Thus, any files in it must fit in the instance's memory.
    file_name = secure_filename(filename)
    return os.path.join(tempfile.gettempdir(), file_name)


# superresImage("images/oma.jpg")
# time = measure(lambda: supperresVideo("images/rotating-boy.gif", "out/vid/video.avi"))

# print("superresing video took: ", time)
