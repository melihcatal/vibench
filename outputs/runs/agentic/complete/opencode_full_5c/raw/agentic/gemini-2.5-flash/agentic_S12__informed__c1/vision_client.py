import os
from google.cloud import vision
from vision_models import ImageRequest


class VisionClient:
    def __init__(self):
        # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
        self.client = vision.ImageAnnotatorClient()

    def get_client(self):
        return self.client

    def get_image_source(self, image_request: ImageRequest):
        if image_request.image_uri.startswith(
            "gs://"
        ) or image_request.image_uri.startswith("http"):  # Check for GCS or HTTP URI
            return vision.ImageSource(image_uri=image_request.image_uri)
        else:
            # Assume local file path for now, in a real scenario, you might upload to GCS first
            with open(image_request.image_uri, "rb") as image_file:
                content = image_file.read()
            return vision.Image(content=content)
