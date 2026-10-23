import os
import requests

from document_models import normalize_text


def check_ocr_text_safety(text):
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]
    url = f"{endpoint.rstrip('/')}/contentsafety/text:analyze?api-version=2024-09-01"
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}
    payload = {
        "text": normalize_text(text),
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
    }
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()
