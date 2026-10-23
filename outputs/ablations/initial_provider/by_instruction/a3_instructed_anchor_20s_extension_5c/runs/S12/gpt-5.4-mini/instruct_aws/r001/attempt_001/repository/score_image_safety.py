from typing import Any, Dict

from vision_client import rekognition_client, load_image_bytes
from vision_models import ImageSource, normalize_safety_response


def score_image_safety(image: ImageSource) -> Dict[str, Any]:
    client = rekognition_client()
    response = client.detect_moderation_labels(Image={"Bytes": load_image_bytes(image)})
    return normalize_safety_response(response)
