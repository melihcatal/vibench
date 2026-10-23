import os
from typing import Dict, List
import requests
from .document_models import OCRResponse


def check_text_safety(text: str) -> Dict:
    """
    Checks extracted document text for unsafe content using Perspective API.
    Requires PERSPECTIVE_API_KEY environment variable.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    data = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
        "languages": ["en"],
    }

    response = requests.post(url, json=data)
    response.raise_for_status()
    return response.json()


def ocr_safety(ocr_response: OCRResponse) -> Dict:
    """
    Checks all text blocks from an OCR response for unsafe content using Perspective API.
    """
    full_text_result = check_text_safety(ocr_response.full_text)
    block_results = []
    for block in ocr_response.blocks:
        block_result = check_text_safety(block.text)
        block_results.append(
            {
                "text": block.text,
                "bounding_box": block.bounding_box,
                "safety_scores": block_result["attributeScores"],
            }
        )

    return {
        "full_text_safety": full_text_result["attributeScores"],
        "block_safety": block_results,
    }
