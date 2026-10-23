import os
import requests
from typing import Dict

from model_models import PerspectiveAPIRequest, PerspectiveAPIResponse


def check_prompt_safety(text: str) -> PerspectiveAPIResponse:
    """Checks prompts and generated text for unsafe content using Perspective API.
    This function will check for various toxicity attributes.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    headers = {"Content-Type": "application/json"}

    # Define the attributes to be checked for toxicity
    attributes = {
        "TOXICITY": {},
        "SEVERE_TOXICITY": {},
        "IDENTITY_ATTACK": {},
        "INSULT": {},
        "PROFANITY": {},
        "THREAT": {},
        "SEXUALLY_EXPLICIT": {},
        "FLIRTATION": {},
    }

    data = {
        "comment": {"text": text},
        "requestedAttributes": attributes,
        "languages": ["en"],
        "doNotStore": True,  # Set to True to prevent Google from storing the text
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()

    return PerspectiveAPIResponse.from_api_response(response.json())
