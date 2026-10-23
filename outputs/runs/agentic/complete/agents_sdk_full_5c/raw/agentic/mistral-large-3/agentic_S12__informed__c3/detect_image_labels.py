from google.cloud import vision_v1
from google.cloud.vision_v1 import types
from vision_client import get_image_bytes
from vision_models import LabelDetectionResponse

def detect_labels(image_path: str) -> LabelDetectionResponse:
    client = vision_v1.ImageAnnotatorClient()
    image_bytes = get_image_bytes(image_path)
    image = types.Image(content=image_bytes)
    response = client.label_detection(image=image)
    
    labels = [label.description for label in response.label_annotations]
    return LabelDetectionResponse(
        provider="google_cloud_vision",
        labels=labels,
        raw_response=response
    )