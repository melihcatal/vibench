# vision_client.py
import os
from google.cloud import vision


class VisionClient:
    def __init__(self):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv(
            "GOOGLE_APPLICATION_CREDENTIALS", "/path/to/credentials.json"
        )
        self.client = vision.ImageAnnotatorClient()

    def label_detection(self, image_path):
        with open(image_path, "rb") as f:
            content = f.read()
        image = vision.Image(content=content)
        response = self.client.label_detection(image=image)
        return [label.description for label in response.label_annotations]

    def safe_search_detection(self, image_path):
        with open(image_path, "rb") as f:
            content = f.read()
        image = vision.Image(content=content)
        response = self.client.safe_search_detection(image=image)
        return response.safe_search_annotation

    def text_detection(self, image_path):
        with open(image_path, "rb") as f:
            content = f.read()
        image = vision.Image(content=content)
        response = self.client.text_detection(image=image)
        return [text.description for text in response.text_annotations]

    def document_text_detection(self, image_path):
        with open(image_path, "rb") as f:
            content = f.read()
        image = vision.Image(content=content)
        response = self.client.document_text_detection(image=image)
        return [block.text for block in response.full_text_annotation.blocks]
