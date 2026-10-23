from __future__ import annotations

from typing import Optional

from vision_client import DEFAULT_MODEL, DEFAULT_PROVIDER, build_image_source, load_vision_client
from vision_models import OCRLine, VisionResult, normalize_confidence


def detect_image_text(path: Optional[str] = None, uri: Optional[str] = None) -> dict:
    client = load_vision_client()
    image, image_meta = build_image_source(path=path, uri=uri)
    response = client.document_text_detection(image=image)

    lines = []
    full_text = response.full_text_annotation
    for page in getattr(full_text, "pages", []):
        for block in getattr(page, "blocks", []):
            for paragraph in getattr(block, "paragraphs", []):
                text = "".join(symbol.text for word in paragraph.words for symbol in word.symbols)
                bbox = [
                    {"x": v.x, "y": v.y}
                    for v in getattr(paragraph.bounding_box, "vertices", [])
                ]
                lines.append(OCRLine(text=text, confidence=normalize_confidence(paragraph.confidence), bounding_box=bbox))

    result = VisionResult(
        provider=DEFAULT_PROVIDER,
        model=DEFAULT_MODEL,
        image=image_meta,
        extracted_text=lines,
        raw_response={"text": getattr(full_text, "text", "")},
    )
    return result.to_dict()
