import os
from google.cloud import vision

class VisionClient:
    def __init__(self, service='vision'):
        # Expect GOOGLE_APPLICATION_CREDENTIALS env var to point at service account JSON
        self.client = vision.ImageAnnotatorClient()
        self.service = service
    
    def label_detection(self, image_path, max_results=10):
        with open(image_path, 'rb') as f:
            image = vision.Image(content=f.read())
        response = self.client.label_detection(image=image, max_results=max_results)
        return response
    
    def document_text_detection(self, image_path):
        with open(image_path, 'rb') as f:
            image = vision.Image(content=f.read())
        response = self.client.document_text_detection(image=image)
        return response
    
    def text_detection(self, image_path):
        with open(image_path, 'rb') as f:
            image = vision.Image(content=f.read())
        response = self.client.text_detection(image=image)
        return response
    
    def safe_search_detection(self, image_path):
        with open(image_path, 'rb') as f:
            image = vision.Image(content=f.read())
        response = self.client.safe_search_detection(image=image)
        return response
