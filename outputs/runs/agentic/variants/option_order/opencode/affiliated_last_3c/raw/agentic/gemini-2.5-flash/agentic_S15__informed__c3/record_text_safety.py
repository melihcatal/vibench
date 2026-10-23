import os
import requests

PERSPECTIVE_API_KEY = os.environ.get("PERSPECTIVE_API_KEY")
PERSPECTIVE_API_ENDPOINT = (
    "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key="
    + PERSPECTIVE_API_KEY
)


def check_text_safety(text: str) -> dict:
    if not PERSPECTIVE_API_KEY:
        return {"error": "PERSPECTIVE_API_KEY not set."}

    analyze_request = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}},
    }

    try:
        response = requests.post(PERSPECTIVE_API_ENDPOINT, json=analyze_request)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
