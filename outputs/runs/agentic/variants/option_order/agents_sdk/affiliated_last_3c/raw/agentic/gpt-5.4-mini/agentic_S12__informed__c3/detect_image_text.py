from __future__ import annotations

from google.cloud import vision

from vision_client import GoogleVisionClient
from vision_models import VisionImageRequest


class TextDetector(GoogleVisionClient):
    def run(self, image_path: str):
        return self.detect_text(VisionImageRequest(image_path=image_path))


vision_provider = vision.ImageAnnotatorClient
