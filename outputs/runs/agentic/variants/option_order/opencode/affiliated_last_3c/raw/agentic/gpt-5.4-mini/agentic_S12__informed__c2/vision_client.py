import os
from functools import lru_cache

from google.cloud import vision


def get_project_id():
    return os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT")


@lru_cache(maxsize=1)
def get_vision_client():
    return vision.ImageAnnotatorClient()


def load_image_content(image_path):
    with open(image_path, "rb") as f:
        return f.read()


def make_image(image_path=None, image_uri=None):
    if image_uri:
        return vision.Image(source=vision.ImageSource(image_uri=image_uri))
    return vision.Image(content=load_image_content(image_path))
