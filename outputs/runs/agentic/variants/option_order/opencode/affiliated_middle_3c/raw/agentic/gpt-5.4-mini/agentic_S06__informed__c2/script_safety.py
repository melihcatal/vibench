import requests

from speech_client import load_config


def check_script_safety(text: str) -> dict:
    cfg = load_config()
    response = requests.post(
        "https://api.perspectiveapi.com/v1/comments:analyze",
        params={"key": cfg.api_key},
        json={"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}},
        timeout=60,
    )
    response.raise_for_status()
    return response.json()
