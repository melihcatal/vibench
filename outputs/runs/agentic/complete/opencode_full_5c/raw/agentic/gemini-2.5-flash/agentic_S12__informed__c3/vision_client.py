import os
from google.cloud import vision


class VisionClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VisionClient, cls).__new__(cls)
            cls._instance.client = vision.ImageAnnotatorClient()
        return cls._instance

    def get_client(self):
        return self.client
