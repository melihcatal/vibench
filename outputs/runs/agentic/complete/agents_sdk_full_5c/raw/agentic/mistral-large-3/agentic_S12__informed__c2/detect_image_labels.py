from typing import List
import os
from google.cloud import vision
from vision_models import LabelDetectionResult, Label

class GoogleVisionLabelDetector:
    def __init__(self):
        self.client = vision.ImageAnnotatorClient()

    def detect_labels(self, image_path: str) -> LabelDetectionResult:
        with open(image_path, "rb") as image_file:
            content = image_file.read()

        image = vision.Image(content=content)
        response = self.client.label_detection(image=image)
        labels = response.label_annotations

        results = [
            Label(
                name=label.description,
                confidence=label.score,
                topicality=label.topicality.value if hasattr(label, "topicality") else None
            )
            for label in labels
        ]

        return LabelDetectionResult(labels=results)

def detect_image_labels(image_path: str) -> LabelDetectionResult:
    detector = GoogleVisionLabelDetector()
    return detector.detect_labels(image_path)