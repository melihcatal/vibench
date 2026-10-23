import os
from google.cloud import vision

class VisionClient:
    def __init__(self):
        # Use Application Default Credentials or explicit env vars
        self.client = vision.ImageAnnotatorClient()
        self.project_id = os.getenv('GOOGLE_CLOUD_PROJECT') or 'my-project'

    def label_detection(self, image_path):
        with open(image_path, 'rb') as f:
            image = vision.Image(content=f.read())
        response = self.client.label_detector.detect(image=image)
        return response

    def image_ocr(self, image_path):
        with open(image_path, 'rb') as f:
            image = vision.Image(content=f.read())
        response = self.client.document_text_detection(image=image)
        return response

    def text_detection(self, image_path):
        with open(image_path, 'rb') as f:
            image = vision.Image(content=f.read())
        response = self.client.text_detector.detect(image=image)
        return response

    def safe_search_detection(self, image_path):
        with open(image_path, 'rb') as f:
            image = vision.Image(content=f.read())
        response = self.client.safe_search_detector.detect(image=image)
        return response

    @staticmethod
    def normalize_labels(response):
        labels = [label.description for label in response.label_annotations]
        return labels

    @staticmethod
    def summarize_description(response):
        # Use the first description if available
        if response.full_text_annotation:
            text = response.full_text_annotation.text.strip()
            return ' '.join(text.split()[:20])  # short snippet
        return ''

    @staticmethod
    def extract_text(response):
        texts = [block.description for page in response.text_annotations
                 for block in page.blocks]
        return [t.strip() for t in texts if t.strip()]

    @staticmethod
    def normalize_safety_score(response):
        # Compute a simple composite unsafe score (0-1)
        unsafe = sum(d.score for d in response.safe_search_annotation if d.adjacency == 'LIKELY')
        return unsafe / 5.0  # assuming max 5 unsafe categories
