from typing import Any, Dict

from vision_client import rekognition_client, load_image_bytes
from vision_models import ImageSource, normalize_detect_labels_response


def detect_image_labels(image: ImageSource) -> Dict[str, Any]:
    client = rekognition_client()
    response = client.detect_labels(Image={"Bytes": load_image_bytes(image)})
    return normalize_detect_labels_response(response)
