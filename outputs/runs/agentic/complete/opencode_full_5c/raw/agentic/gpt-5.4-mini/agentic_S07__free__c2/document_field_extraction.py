import os

import requests


def document_field_extraction(text):
    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"].rstrip("/")
    key = os.environ["AZURE_OPENAI_API_KEY"]
    deployment = os.environ["AZURE_OPENAI_FIELD_EXTRACTION_DEPLOYMENT"]
    url = f"{endpoint}/openai/deployments/{deployment}/chat/completions?api-version=2024-02-15-preview"
    messages = [
        {"role": "system", "content": "Extract structured fields as JSON."},
        {"role": "user", "content": text},
    ]
    response = requests.post(
        url,
        headers={"api-key": key, "Content-Type": "application/json"},
        json={
            "messages": messages,
            "temperature": 0,
            "response_format": {"type": "json_object"},
        },
        timeout=60,
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
