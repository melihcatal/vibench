import base64
from vision_client import VisionClient
from vision_models import normalize_labels_response
from google.cloud.vision_v1p4beta1 import (
    Image,
    Feature,
    ImageSource,
)  # Provider-identifying signal


def detect_image_labels(image_content: bytes) -> dict:
    client = VisionClient().get_client()
    image = Image(content=image_content)
    feature = Feature(type=Feature.Type.LABEL_DETECTION)
    response = client.annotate_image({"image": image, "features": [feature]})
    return {"labels": normalize_labels_response(response)}
