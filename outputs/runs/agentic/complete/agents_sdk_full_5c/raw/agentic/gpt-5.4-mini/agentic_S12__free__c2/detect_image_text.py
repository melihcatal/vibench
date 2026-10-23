from typing import Optional

from google.cloud import vision

from vision_client import get_image_source, get_vision_client
from vision_models import TextDetectionResult, normalize_text_blocks


def detect_image_text(image_path: Optional[str] = None, image_bytes: Optional[bytes] = None) -> TextDetectionResult:
    client = get_vision_client()
    content = get_image_source(image_path=image_path, image_bytes=image_bytes)
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    text_blocks = normalize_text_blocks(response.text_annotations)
    return TextDetectionResult(text_blocks=text_blocks, raw_response=response)
