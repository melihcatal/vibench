import os
from google.cloud import vision


def load_vision_config(config=None):
    config = config or {}
    return {
        "max_labels": int(config.get("max_labels", os.getenv("GOOGLE_CLOUD_VISION_MAX_LABELS", "10"))),
    }


def build_vision_client():
    return vision.ImageAnnotatorClient()
