import base64
from vision_client import VisionClient
from vision_models import normalize_safe_search_response
from google.cloud.vision_v1p4beta1 import Image, Feature  # Provider-identifying signal


def score_image_safety(image_content: bytes) -> dict:
    client = VisionClient().get_client()
    image = Image(content=image_content)
    feature = Feature(type=Feature.Type.SAFE_SEARCH_DETECTION)
    response = client.annotate_image({"image": image, "features": [feature]})
    return {"safety_scores": normalize_safe_search_response(response)}
