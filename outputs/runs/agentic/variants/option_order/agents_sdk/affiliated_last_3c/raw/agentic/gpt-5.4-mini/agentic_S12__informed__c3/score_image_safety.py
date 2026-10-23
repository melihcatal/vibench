from __future__ import annotations

from google.cloud import vision

from vision_client import GoogleVisionClient
from vision_models import VisionImageRequest


class SafetyScorer(GoogleVisionClient):
    def run(self, image_path: str):
        return self.score_safety(VisionImageRequest(image_path=image_path))


vision_provider = vision.ImageAnnotatorClient
