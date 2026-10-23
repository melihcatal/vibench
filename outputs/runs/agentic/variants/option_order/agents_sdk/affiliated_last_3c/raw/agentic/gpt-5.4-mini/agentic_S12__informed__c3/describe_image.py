from __future__ import annotations

from google.cloud import vision

from vision_client import GoogleVisionClient
from vision_models import VisionImageRequest


class ImageDescriber(GoogleVisionClient):
    def run(self, image_path: str):
        return self.describe_image(VisionImageRequest(image_path=image_path, detail="short"))


vision_provider = vision.ImageAnnotatorClient
