import requests
import os

def check_label_safety(text: str) -> dict:
    """Checks secret labels and notes for unsafe text using the Perspective API."
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}}
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()
