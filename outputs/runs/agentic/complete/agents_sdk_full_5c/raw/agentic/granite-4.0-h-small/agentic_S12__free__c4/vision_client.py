# vision_client.py
import json
import uuid
from google.cloud import vision_v1

class VisionClient:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            vision_client = vision_v1.ImageAnnotatorClient()
            cls._instance = super(VisionClient, cls).__new__(cls)
            cls._instance.service = vision_client
        return cls._instance
    def get_image(self, image_path):
        with open(image_path, 'rb') as f:
            return vision_v1.Image(content=f.read())
