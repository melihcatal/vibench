import os

# Explicit provider identification using Google Cloud Vision
from google.cloud import vision_v1 as vision

class VisionClient:
    def __init__(self):
        self.client = vision.ImageAnnotatorClient()

    def label_detection(self, image_path):
        with open(image_path, 'rb') as img_file:
            image = vision.Image(content=img_file.read())
        return self.client.label_detection(image=image).label_annotations

    def annotate_image(self, image_path):
        with open(image_path, 'rb') as img_file:
            image = vision.Image(content=img_file.read())
        response = self.client.annotate_image(
            request={'image': image, 'features': [{'type_': vision.Feature.Type.IMAGE_PROPERTIES}]})
        # Simple caption approximation
        return ' '.join([label.description for label in response.label_annotations])

    def text_extraction(self, image_path):
        with open(image_path, 'rb') as img_file:
            image = vision.Image(content=img_file.read())
        return self.client.text_detection(image=image).text_annotations

    def safe_image_content(self, image_path):
        with open(image_path, 'rb') as img_file:
            image = vision.Image(content=img_file.read())
        analysis = self.client.safe_search_detection(image=image)
        unsafe = any(item.probability > 0 for item in analysis.safe_search_annotation)
        confidence = max(item.probability for item in analysis.safe_search_annotation) if unsafe else 0.0
        return {'unsafe': unsafe, 'confidence': confidence}
