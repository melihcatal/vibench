import os

from google.cloud import vision


def get_vision_client():
    return vision.ImageAnnotatorClient()


def get_default_max_results(name, default):
    value = os.getenv(name)
    return int(value) if value else default


def build_image(payload):
    return vision.Image(content=payload["image_bytes"])
