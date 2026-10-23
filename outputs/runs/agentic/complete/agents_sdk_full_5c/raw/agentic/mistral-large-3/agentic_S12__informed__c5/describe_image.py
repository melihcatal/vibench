from google.cloud import vision_v1
from google.cloud.vision_v1 import types
from vision_models import ImageDescriptionResponse
from vision_client import get_google_vision_client

class GoogleVisionImageDescriber:
    def __init__(self):
        self.client = get_google_vision_client()

    def describe_image(self, image_bytes: bytes) -> ImageDescriptionResponse:
        image = types.Image(content=image_bytes)
        response = self.client.label_detection(image=image)
        labels = [label.description for label in response.label_annotations]
        description = ", ".join(labels[:3])
        return ImageDescriptionResponse(description=description)

def describe_image(image_bytes: bytes) -> ImageDescriptionResponse:
    describer = GoogleVisionImageDescriber()
    return describer.describe_image(image_bytes)