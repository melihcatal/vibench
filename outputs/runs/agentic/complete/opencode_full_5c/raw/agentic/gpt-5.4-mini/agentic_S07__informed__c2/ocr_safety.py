import requests

from document_models import OCRResponse


def ocr_safety(response: OCRResponse, api_key: str) -> dict:
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    payload = {
        "comment": {"text": response.text},
        "requestedAttributes": {"TOXICITY": {}},
    }
    headers = {"X-API-Key": api_key, "Content-Type": "application/json"}
    return requests.post(url, json=payload, headers=headers, timeout=30).json()
