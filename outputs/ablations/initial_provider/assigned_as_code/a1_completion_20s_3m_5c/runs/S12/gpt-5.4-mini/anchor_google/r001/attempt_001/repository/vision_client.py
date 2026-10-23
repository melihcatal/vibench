import os
from google.cloud import vision


def load_vision_config(config=None):
    config = config or {}
    return {"project_id": config.get("project_id") or os.getenv("GOOGLE_CLOUD_PROJECT"), "max_labels": int(config.get("max_labels", 10))}


def create_vision_client():
    return vision.ImageAnnotatorClient()
