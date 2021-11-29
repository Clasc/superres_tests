import base64
from typing import Any

import cv2
import numpy as np
from cv2 import dnn_superres

model = lambda: "res/ESPCN_x4.pb"


def upsampleBase64Img(img_data: str) -> str:
    img = decodeImage(img_data)
    result = upsample(img)
    return encodeImage(result)


def decodeImage(img_data: str):
    data = base64.b64decode(img_data)
    nparr = np.frombuffer(data, np.uint8)
    return cv2.imdecode(nparr, cv2.IMREAD_ANYCOLOR)


def encodeImage(img: Any, extension=".jpg") -> str:
    retval, buffer = cv2.imencode(extension, img)
    if buffer is None:
        print("error encoding image, buffer is empty")
        return ""
    return base64.b64encode(buffer)


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
