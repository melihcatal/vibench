from typing import Optional

from document_client import get_aws_session
from document_models import (
    OcrTextResponse,
    OcrWord,
    OcrLine,
    BoundingBox,
    normalize_bounding_box,
    normalize_confidence,
    join_words_to_lines,
    build_full_text,
)

TEXTRACT_MODEL_ID = "aws.textract.detect_document_text"


def extract_text_from_image(
    image_bytes: bytes,
    feature_types: Optional[list] = None,
) -> OcrTextResponse:
    session, config = get_aws_session()
    textract = session.client("textract", config=config)

    kwargs = {
        "Document": {"Bytes": image_bytes},
    }
    if feature_types:
        kwargs["FeatureTypes"] = feature_types

    response = textract.detect_document_text(**kwargs)

    words = []
    lines_raw = []

    for block in response.get("Blocks", []):
        if block["BlockType"] == "WORD":
            bbox = _parse_bounding_box(block.get("Geometry", {}).get("Polygon", []))
            word = OcrWord(
                text=block.get("Text", ""),
                confidence=normalize_confidence(block.get("Confidence")),
                bounding_box=bbox,
            )
            words.append(word)
        elif block["BlockType"] == "LINE":
            lines_raw.append(block)

    ocr_lines = join_words_to_lines(words)

    full_text = build_full_text(ocr_lines)

    avg_confidence = 0.0
    if words:
        avg_confidence = sum(w.confidence for w in words) / len(words)

    page_width = 1.0
    page_height = 1.0

    return OcrTextResponse(
        full_text=full_text,
        lines=ocr_lines,
        words=words,
        page_width=page_width,
        page_height=page_height,
        confidence=normalize_confidence(avg_confidence),
    )


def extract_text_from_s3(
    bucket: str,
    key: str,
) -> OcrTextResponse:
    session, config = get_aws_session()
    textract = session.client("textract", config=config)

    response = textract.detect_document_text(
        Document={
            "S3Object": {
                "Bucket": bucket,
                "Name": key,
            }
        }
    )

    words = []
    for block in response.get("Blocks", []):
        if block["BlockType"] == "WORD":
            bbox = _parse_bounding_box(block.get("Geometry", {}).get("Polygon", []))
            word = OcrWord(
                text=block.get("Text", ""),
                confidence=normalize_confidence(block.get("Confidence")),
                bounding_box=bbox,
            )
            words.append(word)

    ocr_lines = join_words_to_lines(words)
    full_text = build_full_text(ocr_lines)

    avg_confidence = 0.0
    if words:
        avg_confidence = sum(w.confidence for w in words) / len(words)

    return OcrTextResponse(
        full_text=full_text,
        lines=ocr_lines,
        words=words,
        page_width=1.0,
        page_height=1.0,
        confidence=normalize_confidence(avg_confidence),
    )


def _parse_bounding_box(polygon: list) -> BoundingBox:
    if not polygon:
        return BoundingBox(x=0.0, y=0.0, width=0.0, height=0.0)
    points = [(p["X"], p["Y"]) for p in polygon]
    return normalize_bounding_box(points)
