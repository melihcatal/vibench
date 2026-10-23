from __future__ import annotations

import requests

from security_client import get_http_session
from security_models import normalize_text_payload

PERSPECTIVE_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_payload_safety(text: str) -> dict:
    session = get_http_session()
    payload = normalize_text_payload(text)
    response = session.post(PERSPECTIVE_ENDPOINT, params={"key": "${PERSPECTIVE_API_KEY}"}, json={"comment": {"text": payload}, "requestedAttributes": {"TOXICITY": {}}}, timeout=30)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    pass
