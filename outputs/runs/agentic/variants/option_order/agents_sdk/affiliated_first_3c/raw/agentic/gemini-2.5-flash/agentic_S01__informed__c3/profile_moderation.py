import requests
import os

def moderate_profile_text(text: str) -> dict:
    perspective_api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not perspective_api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={perspective_api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}}
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to moderate profile text: {e}")
