import os
import requests


def moderate_vendor_text_safety(text: str) -> dict:
    """
    Moderates vendor notes or memo fields using the Perspective API.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = (
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key="
        + api_key
    )

    # See https://developers.perspectiveapi.com/s/about-the-api-attributes-and-languages
    # for available attributes.
    requested_attributes = {
        "TOXICITY": {},
        "SEVERE_TOXICITY": {},
        "THREAT": {},
        "INSULT": {},
        "PROFANITY": {},
    }

    data = {
        "comment": {"text": text},
        "requestedAttributes": requested_attributes,
        "languages": ["en"],  # Specify language, e.g., English
    }

    response = requests.post(url, json=data)
    response.raise_for_status()  # Raise an exception for HTTP errors

    return response.json()
