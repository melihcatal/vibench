from __future__ import annotations

from typing import Dict, List, Optional

from vision_client import build_vision_image, get_google_vision_client
from vision_models import normalize_ocr_blocks


PROVIDER = "google_cloud_vision"


def detect_image_text(image_path: Optional[str] = None, image_uri: Optional[str] = None) -> List[Dict[str, object]]:
    client = get_google_vision_client()
    image = build_vision_image(image_path=image_path, image_uri=image_uri)
    response = client.text_detection(image=image)
    blocks = []
    for annotation in response.text_annotations[1:]:
        blocks.append(
            {
                "text": annotation.description,
                "confidence": 1.0,
                "block_type": "word",
            }
        )
    if not blocks and response.full_text_annotation.text:
        blocks.append({"text": response.full_text_annotation.text, "confidence": 1.0, "block_type": "document"})
    return normalize_ocr_blocks(blocks)
