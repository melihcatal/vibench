# document_field_extraction.py
import os
import json
from typing import Any, List, Dict

# Local helpers
from document_client import DocumentClient
from document_models import OCRResult, LayoutResult

# Alibaba Cloud OCR API (REST) base URL
ALIBABA_OCR_URL = 'https://vision-gov-cn-shanghai.service.software.baidubce.com/v1/ocr/govcn/doc'
# Placeholder credentials (replace with your real ones)
ALIBABA_ACCESS_KEY_ID = os.getenv('ALIBABA_ACCESS_KEY_ID')
ALIBABA_ACCESS_KEY_SECRET = os.getenv('ALIBABA_ACCESS_KEY_SECRET')


def call_alibaba_ocr(image_path: str) -> Dict[str, Any]:
    """Call Alibaba Cloud OCR for general document text and structured fields."""
    if not (ALIBABA_ACCESS_KEY_ID and ALIBABA_ACCESS_KEY_SECRET):
        raise RuntimeError('Set ALIBABA_ACCESS_KEY_ID and ALIBABA_ACCESS_KEY_SECRET for OCR')
    # Alibaba Cloud SDK usually handles signing; here we simulate a plain request
    # In production, use alibabacloud_ocr_api SDK for automatic authentication.
    # We'll use the `requests` library to showcase integration.
    # Build multipart/form-data payload
    import requests
    files = {'file': open(image_path, 'rb')}
    # Alibaba expects parameters in query string for API key
    params = {
        'accessKeyId': ALIBABA_ACCESS_KEY_ID,
        # 'signature' and other auth details handled by SDK in real use
    }
    # NOTE: This endpoint format is illustrative; actual Alibaba OCR endpoint differs.
    response = requests.post(ALIBABA_OCR_URL, files=files, params=params)
    response.raise_for_status()
    return response.json()


def extract_fields(text: str) -> List[Dict[str, Any]]:
    """Simple rule‑based extraction of field names and values from normalized text.
    This works for forms where field names end with a colon. The function returns a list
    of dictionaries, each containing 'field' and 'value'.
    """
    field_pattern = r'([\w\s]+):\s*(.*)\n'
    import re
    matches = re.findall(field_pattern, text, re.MULTILINE)
    fields = []
    for key, value in matches:
        fields.append({'field': key.strip(), 'value': value.strip()})
    return fields


def extract_fields_from_ocr(ocr_result: OCRResult) -> List[Dict[str, Any]]:
    """Combine OCR result with layout hints and return structured fields."""
    # For demo we only use raw_text; a richer implementation could use page layout
    raw = ocr_result.raw_text
    return extract_fields(raw)

# Demo / integration example
if __name__ == '__main__':
    # Assume we already have OCR results (placeholder)
    sample_ocr = OCRResult(raw_text='Name: John Doe\nDate: 2024-07-15\nAmount: $100.00', layout_result=None)
    print('Extracted fields:', extract_fields_from_ocr(sample_ocr))
    # Real usage would call Alibaba OCR first
    # alibaba_response = call_alibaba_ocr('sample_invoice.pdf')
    # print('Alibaba OCR JSON:', json.dumps(alibaba_response, indent=2))