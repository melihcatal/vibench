import requests

from document_client import load_config


def ocr_safety(text: str) -> dict:
    config = load_config()
    response = requests.post(
        f"{config.endpoint}/contentsafety/text:analyze?api-version=2024-09-01",
        headers={
            "Ocp-Apim-Subscription-Key": config.api_key or "",
            "Content-Type": "application/json",
        },
        json={"text": text},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
