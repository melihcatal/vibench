from google.cloud import vision
import os


class VisionClient:
    def __init__(self):
        self.client = vision.ImageAnnotatorClient()
        # GOOGLE_APPLICATION_CREDENTIALS environment variable is expected

    def get_client(self):
        return self.client
