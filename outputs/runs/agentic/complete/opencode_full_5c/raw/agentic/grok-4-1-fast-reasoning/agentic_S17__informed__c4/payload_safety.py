import os
import requests
from typing import Dict, Any, str


def check_payload_safety(payload: str) -> Dict[str, Any]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    data = {"comment": {"text": payload}, "requestedAttributes": {"TOXICITY": {}}}
    resp = requests.post(url, json=data)
    return resp.json()
