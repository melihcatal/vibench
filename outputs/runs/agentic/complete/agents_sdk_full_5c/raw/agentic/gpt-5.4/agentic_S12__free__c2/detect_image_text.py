from __future__ import annotations

from typing import List, Dict

from google.cloud.vision_v1 import Image

from vision_client import build_google_vision_client, load_image_source
from vision_models import normalize_text_blocks


GOOGLE_VISION_PROVIDER = "vision.googleapis.com"


def detect_image_text(image_path: str) -> List[Dict[str, float]]:
    source = load_image_source(image_path)
    client = build_google_vision_client()
    response = client.text_detection(image=Image(content=source.image_bytes))
    if response.error.message:
        raise RuntimeError(response.error.message)
    blocks = []
    for annotation in response.text_annotations[1:]:
        blocks.append({"text": annotation.description, "score": getattr(annotation, "confidence", 0.0)})
    if not blocks and response.text_annotations:
        blocks.append({"text": response.text_annotations[0].description, "score": 1.0})
    return normalize_text_blocks(blocks)
