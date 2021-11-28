from flask import Request
from utils.upsample import upsampleBase64Img


def upscale(data: bytes):
    return upsampleBase64Img(data)
