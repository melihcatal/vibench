import base64
import os
from typing import Optional

from google.cloud import vision

from vision_client import get_image_source, get_vision_client
from vision_models import LabelDetectionResult, normalize_labels


def detect_image_labels(image_path: Optional[str] = None, image_bytes: Optional[bytes] = None) -> LabelDetectionResult:
    client = get_vision_client()
    content = get_image_source(image_path=image_path, image_bytes=image_bytes)
    image = vision.Image(content=content)
    response = client.label_detection(image=image)
    labels = normalize_labels(response.label_annotations)
    return LabelDetectionResult(labels=labels, raw_response=response)


def detect_from_base64(image_base64: str) -> LabelDetectionResult:
    return detect_image_labels(image_bytes=base64.b64decode(image_base64))
e_base64))
