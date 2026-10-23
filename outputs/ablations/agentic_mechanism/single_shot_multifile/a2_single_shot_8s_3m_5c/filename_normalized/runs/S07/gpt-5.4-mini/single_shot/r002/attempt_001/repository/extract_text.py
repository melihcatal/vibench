import base64
import os
from typing import Optional

import requests

from document_client import build_document_request_headers, get_ocr_endpoint, load_document_bytes
from document_models import OcrResult, parse_textract_detect_document_text_response


def extract_text(document_path: str, mime_type: Optional[str] = None) -> OcrResult:
    content = load_document_bytes(document_path)
    endpoint = get_ocr_endpoint("detect-document-text")
    headers = build_document_request_headers(content, mime_type=mime_type)
    response = requests.post(endpoint, headers=headers, data=content, timeout=120)
    response.raise_for_status()
    return parse_textract_detect_document_text_response(response.json())
