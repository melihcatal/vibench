import os
import requests


def check_platform_output_safety(text: str) -> dict:
    endpoint = "https://api.perspectiveapi.com/v1alpha1/comments:analyze"
    api_key = os.getenv("PERSPECTIVE_API_KEY", "")
    payload = {"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}}
    response = requests.post(
        endpoint, params={"key": api_key}, json=payload, timeout=30
    )
    response.raise_for_status()
    return response.json()
