from __future__ import annotations

from typing import Optional

from google.cloud import vision

from vision_client import DEFAULT_PROVIDER, get_vision_client, make_vision_image
from vision_models import DetectionResult, OCRLine


def detect_image_text(image_path: Optional[str] = None, image_bytes: Optional[bytes] = None) -> dict:
    client = get_vision_client()
    image = make_vision_image(image_path=image_path, image_bytes=image_bytes)
    response = client.document_text_detection(image=image)
    if response.error.message:
        raise RuntimeError(response.error.message)

    lines = []
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                text = "".join(symbol.text for word in paragraph.words for symbol in word.symbols)
                confidence = float(paragraph.confidence)
                if text.strip():
                    lines.append(OCRLine(text=text, confidence=confidence))

    result = DetectionResult(
        provider=DEFAULT_PROVIDER,
        image_uri=image_path,
        ocr_lines=lines,
        raw={"full_text": response.full_text_annotation.text},
    )
    return result.to_dict()
