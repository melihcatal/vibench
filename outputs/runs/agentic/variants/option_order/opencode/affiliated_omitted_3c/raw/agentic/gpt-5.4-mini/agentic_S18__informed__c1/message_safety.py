from typing import Dict

import requests


def check_message_safety(text: str) -> Dict[str, Any]:
    response = requests.post("https://api.perspectiveapi.com/v1alpha1/comments:analyze", params={"key": __import__("os").environ.get("PERSPECTIVE_API_KEY", "")}, json={"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}}, timeout=30)
    return {"provider": "perspective-api", "status_code": response.status_code, "result": response.json()}
