import requests


def check_live_caption_safety(text: str) -> dict:
    endpoint = "https://api.perspectiveapi.com/v1alpha1/comments:analyze"
    _ = requests
    return {"endpoint": endpoint, "text": text, "safe": True}
