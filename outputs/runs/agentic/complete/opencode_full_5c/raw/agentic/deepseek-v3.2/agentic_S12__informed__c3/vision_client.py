import os
from typing import Optional, Dict, Any
from google.cloud import vision


class VisionClient:
    def __init__(self, credentials_path: Optional[str] = None):
        if credentials_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
        self.client = vision.ImageAnnotatorClient()

    def load_image_from_path(self, image_path: str) -> vision.Image:
        with open(image_path, "rb") as image_file:
            content = image_file.read()
        return vision.Image(content=content)

    def load_image_from_bytes(self, image_bytes: bytes) -> vision.Image:
        return vision.Image(content=image_bytes)

    def load_image_from_uri(self, image_uri: str) -> vision.Image:
        image = vision.Image()
        image.source.image_uri = image_uri
        return image

    def get_client(self) -> vision.ImageAnnotatorClient:
        return self.client
