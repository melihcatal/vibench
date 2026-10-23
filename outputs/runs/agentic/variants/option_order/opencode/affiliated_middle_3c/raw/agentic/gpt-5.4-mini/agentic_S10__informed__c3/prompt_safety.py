import os
import requests


def check_prompt_safety(text: str) -> dict:
    endpoint = "https://api.perspectiveapi.com/v1alpha1/comments:analyze"
    key = os.getenv("PERSPECTIVE_API_KEY", "")
    payload = {"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}}
    response = requests.post(f"{endpoint}?key={key}", json=payload, timeout=30)
    response.raise_for_status()
    return response.json()
