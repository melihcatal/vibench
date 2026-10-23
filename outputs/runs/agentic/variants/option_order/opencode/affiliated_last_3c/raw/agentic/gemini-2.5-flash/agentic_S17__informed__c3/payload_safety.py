import requests
import os


def check_payload_safety(text_payload: str) -> dict:
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = (
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key="
        + api_key
    )

    # The request to Perspective API includes the text content and requested attribute scores.
    # See https://developers.perspectiveapi.com/s/about-the-api-attributes for available attributes.
    data = {
        "comment": {"text": text_payload},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "THREAT": {},
            "SEXUALLY_EXPLICIT": {},
            "FLIRTATION": {},
            "ATTACK_ON_AUTHOR": {},
            "ATTACK_ON_COMMENTER": {},
        },
    }

    response = requests.post(url, json=data)
    response.raise_for_status()

    return response.json()
