import time
import cv2
from cv2 import CAP_PROP_TILT, THRESH_TOZERO, dnn_superres


def path():
    return "res/ESPCN_x4.pb"


def create_superSampler():
    sr = cv2.dnn_superres.DnnSuperResImpl_create()
    sr.readModel(path())
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


def supperresVideo(input: str, out: str):
    frames = vidToFrames(input)
    frames = upresList(frames)
    writeFrames(frames, out)


# superresImage("images/oma.jpg")
time = measure(lambda: supperresVideo("images/rotating-boy.gif", "out/vid/video.avi"))

print("superresing video took: ", time)
