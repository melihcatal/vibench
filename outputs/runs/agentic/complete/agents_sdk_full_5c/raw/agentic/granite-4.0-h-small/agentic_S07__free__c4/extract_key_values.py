# [SAME-SCENARIO] extract_key_values.py

import os
from typing import List, Dict
from google.cloud import vision_v1
from .document_client import VisionClient
from .document_models import KeyValueExtractionResponse

def extract_key_values(image_bytes: bytes) -> KeyValueExtractionResponse:
    """Extract key-value pairs from a form-like document using Google Cloud Vision Key-Value Pair entity detection.

    Args:
        image_bytes: raw image data.
    
    Returns:
        A KeyValueExtractionResponse containing detected key-value entities.
    """
    client = VisionClient()
    image = vision_v1.types.Image(content=image_bytes)
    # Use product search style or document text detection with field settings if available
    # For simplicity we reuse OCR response and filter for KV entities manually
    response = client.service.document_text_detection(image=image)
    kv_pairs = []
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            # Simplified heuristic: assume first line is key, second line is value
            if len(block.words) >= 2:
                key = block.words[0].symbols[0].text
                value = block.words[1].symbols[0].text
                kv_pairs.append({"key": key, "value": value})
    return KeyValueExtractionResponse(key_value_pairs=kv_pairs)
