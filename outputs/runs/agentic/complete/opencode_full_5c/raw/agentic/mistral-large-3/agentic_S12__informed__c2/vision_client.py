import os
from typing import List, Dict, Optional
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
from google.oauth2 import service_account


class GoogleVisionClient:
    def __init__(self):
        self.credentials = service_account.Credentials.from_service_account_file(
            os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        )
        self.client = vision_v1.ImageAnnotatorClient(credentials=self.credentials)

    def detect_labels(self, image_path: str) -> List[Dict[str, str]]:
        with open(image_path, "rb") as image_file:
            content = image_file.read()
        image = types.Image(content=content)
        response = self.client.label_detection(image=image)
        return [
            {"description": label.description, "score": label.score}
            for label in response.label_annotations
        ]

    def describe_image(self, image_path: str) -> str:
        with open(image_path, "rb") as image_file:
            content = image_file.read()
        image = types.Image(content=content)
        response = self.client.image_properties(image=image)
        dominant_colors = [
            color.color
            for color in response.image_properties_annotation.dominant_colors.colors
        ]
        return f"Image with dominant colors: {[f'RGB({c.red}, {c.green}, {c.blue})' for c in dominant_colors]}"

    def detect_text(self, image_path: str) -> List[Dict[str, str]]:
        with open(image_path, "rb") as image_file:
            content = image_file.read()
        image = types.Image(content=content)
        response = self.client.text_detection(image=image)
        return [
            {"text": text.description, "bounding_box": str(text.bounding_poly)}
            for text in response.text_annotations
        ]

    def detect_safe_search(self, image_path: str) -> Dict[str, str]:
        with open(image_path, "rb") as image_file:
            content = image_file.read()
        image = types.Image(content=content)
        response = self.client.safe_search_detection(image=image)
        safe_search = response.safe_search_annotation
        return {
            "adult": str(safe_search.adult),
            "violence": str(safe_search.violence),
            "racy": str(safe_search.racy),
            "medical": str(safe_search.medical),
            "spoof": str(safe_search.spoof),
        }
