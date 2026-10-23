import os
import requests

from document_models import normalize_text


def check_ocr_safety(text: str) -> dict:
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]
    response = requests.post(
        f"{endpoint}/contentsafety/text:analyze?api-version=2024-09-01",
        headers={"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"},
        json={"text": normalize_text(text)},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
