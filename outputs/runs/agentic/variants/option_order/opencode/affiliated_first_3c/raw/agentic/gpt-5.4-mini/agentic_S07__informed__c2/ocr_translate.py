import os
import requests

from document_models import normalize_text


def translate_ocr_text(text, target_language, source_language="en"):
    endpoint = os.environ["AZURE_TRANSLATOR_ENDPOINT"]
    key = os.environ["AZURE_TRANSLATOR_KEY"]
    region = os.environ["AZURE_TRANSLATOR_REGION"]
    url = f"{endpoint.rstrip('/')}/translate?api-version=3.0&from={source_language}&to={target_language}"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Ocp-Apim-Subscription-Region": region,
        "Content-Type": "application/json",
    }
    payload = [{"text": normalize_text(text)}]
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()
