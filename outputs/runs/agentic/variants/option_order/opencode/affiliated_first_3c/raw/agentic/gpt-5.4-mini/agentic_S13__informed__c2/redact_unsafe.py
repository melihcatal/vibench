import requests

from safety_client import auth_headers, endpoint_url, has_safety_credentials
from safety_models import RedactionSpan, normalize_text


def redact_unsafe(text: str):
    text = normalize_text(text)
    payload = {"text": text, "redactionPolicy": "mask"}
    if has_safety_credentials():
        response = requests.post(
            endpoint_url("/contentsafety/text:redact"),
            json=payload,
            headers=auth_headers(),
            timeout=30,
        )
        response.raise_for_status()
        return response.json()
    return {"text": text, "redactedText": text, "spans": []}
