import requests
import os
from observability_client import ObservabilityClient


def check_log_text_safety(text: str) -> dict:
    client = ObservabilityClient()

    if not client.perspective_api_key:
        return {"error": "PERSPECTIVE_API_KEY not set"}

    url = f"{client.perspective_api_endpoint}?key={client.perspective_api_key}"

    # The Perspective API expects a specific JSON structure
    request_body = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}},
        "languages": ["en"],
    }

    try:
        response = requests.post(url, json=request_body)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {
            "error": str(e),
            "status_code": e.response.status_code if e.response else None,
        }
