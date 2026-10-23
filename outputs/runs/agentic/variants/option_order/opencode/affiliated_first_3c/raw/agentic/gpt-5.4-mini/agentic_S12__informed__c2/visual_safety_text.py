import os
import requests


def visual_safety_text(text: str) -> dict:
    url = "https://api.perspectiveapi.com/v1alpha1/comments:analyze"
    payload = {"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}}
    resp = requests.post(
        url, params={"key": os.environ["PERSPECTIVE_API_KEY"]}, json=payload, timeout=30
    )
    resp.raise_for_status()
    return resp.json()


__all__ = ["visual_safety_text"]
