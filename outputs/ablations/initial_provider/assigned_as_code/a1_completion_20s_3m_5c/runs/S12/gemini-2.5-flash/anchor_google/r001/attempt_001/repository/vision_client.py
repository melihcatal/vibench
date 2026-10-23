from google.cloud import vision
import os

class VisionClient:
    def __init__(self):
        # Google Cloud Vision API client is implicitly authenticated via GOOGLE_APPLICATION_CREDENTIALS
        # or by running in a Google Cloud environment.
        self._client = vision.ImageAnnotatorClient()

    def get_image_annotator_client(self):
        return self._client
