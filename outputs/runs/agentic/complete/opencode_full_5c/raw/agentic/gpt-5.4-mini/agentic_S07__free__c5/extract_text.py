import os
from typing import Any, Dict
from document_client import get_client, load_image_bytes
from document_models import OCRRequest, OCRResponse, normalize_ocr_result


def extract_text(image_path: str, language_code: str = 'en') -> Dict[str, Any]:
    client = get_client()
    payload = OCRRequest(image_bytes=load_image_bytes(image_path), language_code=language_code)
    result = client.extract_text(payload)
    return normalize_ocr_result(result).to_dict()
