import os
import tempfile
import cv2
import numpy as np
import base64
from cv2 import FileStorage, dnn_superres
from werkzeug.utils import secure_filename

model = lambda: "res/ESPCN_x4.pb"


def upsampleBase64Img(img_data: bytes) -> bytes:
    nparr = np.fromstring(img_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    result = upsample(img)
    return cv2.imencode("jpg", result)


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


def get_file_path(filename):
    # Note: tempfile.gettempdir() points to an in-memory file system
    # on GCF. Thus, any files in it must fit in the instance's memory.
    file_name = secure_filename(filename)
    return os.path.join(tempfile.gettempdir(), file_name)
