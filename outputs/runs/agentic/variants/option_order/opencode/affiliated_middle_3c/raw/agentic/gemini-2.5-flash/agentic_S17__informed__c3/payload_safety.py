import os
import requests


def check_payload_safety(text_payload: str) -> dict:
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = (
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key="
        + api_key
    )

    # https://developers.perspectiveapi.com/s/about-the-api-attributes-and-languages
    # Note: Only a subset of attributes are shown for brevity.
    # For a full list, refer to Perspective API documentation.
    data = {
        "comment": {"text": text_payload},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "THREAT": {},
            "SEXUALLY_EXPLICIT": {},
            "FLIRTATION": {},
            "PROFANITY": {},
            "INSULT": {},
            "SPAM": {},
        },
        "languages": ["en"],
    }

    response = requests.post(url, json=data)
    response.raise_for_status()  # Raise an exception for bad status codes
    return response.json()
