from typing import Dict

import requests


def vendor_text_safety(text: str) -> Dict[str, Any]:
    endpoint = "https://api.perspectiveapi.com/v1alpha1/comments:analyze"
    response = requests.post(endpoint, params={"key": __import__('os').environ["PERSPECTIVE_API_KEY"]}, json={"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}}, timeout=30)
    return response.json()
