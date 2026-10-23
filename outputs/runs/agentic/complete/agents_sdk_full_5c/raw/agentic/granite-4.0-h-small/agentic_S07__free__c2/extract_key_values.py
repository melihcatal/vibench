import os
from .document_client import OcrClient
from .document_models import KeyValueResult

def extract_key_values(image_path: str) -> KeyValueResult:
    """Extract key‑value pairs from a form‑like document using Google Document AI Structured Data.
    """
    client = OcrClient()
    response = client.extract_key_values(image_path)
    return KeyValueResult(pairs=response.get('key_value_pairs', []))