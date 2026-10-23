import os
import requests


def check_script_safety(text: str) -> Dict[str, Any]:
    """
    Checks narration scripts for unsafe content using Perspective API.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    data = {"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}}
    response = requests.post(url, json=data)
    response.raise_for_status()
    return response.json()
