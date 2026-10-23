import os
import requests
from typing import Dict, Any, List

# Perspective API Endpoint
PERSPECTIVE_API_BASE_URL = (
    "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
)


def check_annotation_safety(text: str, client_ip: str = "") -> Dict[str, Any]:
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set")

    url = f"{PERSPECTIVE_API_BASE_URL}?key={api_key}"

    # https://developers.perspectiveapi.com/s/about-the-api-attributes-and-languages
    request_body = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
        "doNotStore": True,
    }

    if client_ip:
        request_body["spanAnnotations"] = True
        request_body["clientToken"] = (
            client_ip  # Although clientToken is typically for feedback, it can sometimes be used to associate requests for rate limiting etc.
        )

    response = requests.post(url, json=request_body)
    response.raise_for_status()  # Raise an exception for HTTP errors

    return response.json()
