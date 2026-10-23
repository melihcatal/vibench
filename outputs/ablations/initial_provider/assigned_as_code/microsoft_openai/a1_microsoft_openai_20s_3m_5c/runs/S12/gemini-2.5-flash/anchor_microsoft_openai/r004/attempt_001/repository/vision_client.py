from google.cloud import vision
import os

class VisionClient:
    def __init__(self):
        self._client = vision.ImageAnnotatorClient()

    def get_client(self):
        return self._client
