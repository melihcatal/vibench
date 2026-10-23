from __future__ import annotations

from google.cloud import vision

from vision_client import GoogleVisionClient
from vision_models import VisionImageRequest


class LabelDetector(GoogleVisionClient):
    def run(self, image_path: str):
        request = VisionImageRequest(image_path=image_path, max_results=10)
        return self.detect_labels(request)


vision_provider = vision.ImageAnnotatorClient
