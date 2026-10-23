import json
import requests


def extract_key_values(document_text):
    """Extract key-value pairs from a form-like document using Mindee OCR API."""
    api_key = "MINDEE_API_KEY"  # placeholder, configure via env if desired
    url = "https://api.mined.ai/v2/document"
    payload = {"file": ("document.jpg", open(document_text, "rb"), "image/jpeg")}
    headers = {"Authorization": f"Apikey {api_key}"}
    response = requests.post(url, files=payload, headers=headers)
    data = response.json()
    # Normalize to a simple dict of key:value strings
    kv = {}
    for field in data["document"]["fields"]:
        kv[field["id"]] = field["value"]
    return kv
