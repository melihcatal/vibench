from __future__ import annotations

from typing import List, Optional

from vision_client import GOOGLE_VISION_PROVIDER, build_google_image, get_google_vision_client, load_image_source
from vision_models import OCRTextBlock, normalize_google_ocr


PROVIDER = GOOGLE_VISION_PROVIDER


def detect_image_text(*, image_path: Optional[str] = None, image_uri: Optional[str] = None) -> List[OCRTextBlock]:
    client = get_google_vision_client()
    image = build_google_image(load_image_source(image_path=image_path, image_uri=image_uri))
    response = client.text_detection(image=image)
    if response.error.message:
        raise RuntimeError(response.error.message)
    return normalize_google_ocr(response)
