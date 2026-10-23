import os

import requests


def extract_document_fields(text: str) -> dict:
    endpoint = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
    api_key = os.getenv("OPENAI_API_KEY", "")
    response = requests.post(
        f"{endpoint}/responses",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "model": "gpt-5.4-mini",
            "input": f"Extract structured fields as JSON from the following OCR text:\n{text}",
        },
        timeout=120,
    )
    response.raise_for_status()
    return response.json()
