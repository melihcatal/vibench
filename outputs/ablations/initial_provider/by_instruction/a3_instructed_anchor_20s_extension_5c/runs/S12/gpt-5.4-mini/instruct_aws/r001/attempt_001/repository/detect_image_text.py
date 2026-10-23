from typing import Any, Dict

from vision_client import rekognition_client, load_image_bytes
from vision_models import ImageSource, normalize_text_detection_response


def detect_image_text(image: ImageSource) -> Dict[str, Any]:
    client = rekognition_client()
    response = client.detect_text(Image={"Bytes": load_image_bytes(image)})
    return normalize_text_detection_response(response)
