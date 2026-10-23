import os
import requests
import json
from security_models import ContentSafetyRequest

# Perspective API endpoint and key
PERSPECTIVE_API_BASE_URL = (
    "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
)


def check_secret_label_safety(request: ContentSafetyRequest) -> dict:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"{PERSPECTIVE_API_BASE_URL}?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {
        "comment": {"text": request.text_content},
        "requestedAttributes": {"TOXICITY": {}},
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    return response.json()
