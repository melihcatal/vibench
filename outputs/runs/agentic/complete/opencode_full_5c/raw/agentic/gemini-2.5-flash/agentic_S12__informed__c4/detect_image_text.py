import base64
from vision_client import VisionClient
from vision_models import normalize_text_detection_response
from google.cloud.vision_v1p4beta1 import Image, Feature  # Provider-identifying signal


def detect_image_text(image_content: bytes) -> dict:
    client = VisionClient().get_client()
    image = Image(content=image_content)
    feature = Feature(type=Feature.Type.TEXT_DETECTION)
    response = client.annotate_image({"image": image, "features": [feature]})
    return {"text": normalize_text_detection_response(response)}
