from google.cloud import vision

class DocumentClient:
    def __init__(self):
        self.client = vision.ImageAnnotatorClient()
