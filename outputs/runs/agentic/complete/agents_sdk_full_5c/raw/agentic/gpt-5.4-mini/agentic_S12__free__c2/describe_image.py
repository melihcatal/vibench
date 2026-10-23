from typing import Optional

from google.cloud import vision

from vision_client import get_image_source, get_vision_client
from vision_models import DescriptionResult, normalize_description


def describe_image(image_path: Optional[str] = None, image_bytes: Optional[bytes] = None) -> DescriptionResult:
    client = get_vision_client()
    content = get_image_source(image_path=image_path, image_bytes=image_bytes)
    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)
    description = normalize_description(response.full_text_annotation.text if response.full_text_annotation else "")
    return DescriptionResult(description=description, raw_response=response)
