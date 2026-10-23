import os
from typing import Any, Dict, Optional

import boto3

from document_client import build_textract_client, load_bytes, normalize_ocr_text
from document_models import DocumentRequest, TextExtractionResult


def extract_text(source: Any, *, region_name: Optional[str] = None) -> TextExtractionResult:
    request = DocumentRequest.from_input(source)
    client = build_textract_client(region_name=region_name)
    response = client.detect_document_text(Document={"Bytes": load_bytes(request)})
    text = normalize_ocr_text(response)
    return TextExtractionResult(text=text, raw=response)
