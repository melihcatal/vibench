# [LATER-STEP] ocr_safety.py

import openai
from document_client import DocumentClient
from document_models import OCRRequest, normalize_ocr_response


def scan_for_unsafe_content(image_path: str) -> bool:
    """Check OCR text from a scanned document for unsafe or disallowed content.

    Args:
        image_path: Path to the scanned image.

    Returns:
        True if unsafe content is detected, False otherwise.
    """
    client = DocumentClient()
    raw_text = client.extract_text(image_path)
    lines = normalize_ocr_response(raw_text)
    text = "\\n".join(lines)
    # Simple safety check using content filter (OpenAI moderation endpoint)
    moderation = openai.Moderation.create(input=text)
    return moderation.results[0].flagged
