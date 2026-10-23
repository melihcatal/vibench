from google.cloud import vision

class VisionModel:
    def __init__(self, client):
        self.client = client

    def label_detection(self, image):
        response = self.client.label_detection(image=image)
        return response.label_annotations

    def text_detection(self, image):
        response = self.client.text_detection(image=image)
        return response.text_annotations

    def safe_search_detection(self, image):
        response = self.client.safe_search_detection(image=image)
        return response.safe_search_annotation