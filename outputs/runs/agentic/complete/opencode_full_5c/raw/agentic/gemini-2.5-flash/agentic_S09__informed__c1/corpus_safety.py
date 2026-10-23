import os
import requests
from typing import List, Dict, Any

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
PERSPECTIVE_API_ENDPOINT = (
    "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
)


def check_corpus_safety(text: str) -> Dict[str, Any]:
    """Checks the safety of a given text using the Perspective API.

    Args:
        text: The text string to check.

    Returns:
        A dictionary containing the safety analysis results from Perspective API.
    """
    if not PERSPECTIVE_API_KEY:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    params = {"key": PERSPECTIVE_API_KEY}
    data = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
            "SEXUALLY_EXPLICIT": {},
            "FLIRTATION": {},
        },
        "languages": ["en"],
    }

    headers = {"Content-Type": "application/json"}

    response = requests.post(
        PERSPECTIVE_API_ENDPOINT, params=params, json=data, headers=headers
    )
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()


def batch_check_corpus_safety(texts: List[str]) -> List[Dict[str, Any]]:
    """Checks the safety of a batch of texts using the Perspective API.

    Args:
        texts: A list of text strings to check.

    Returns:
        A list of dictionaries, each containing the safety analysis results for a corresponding text.
    """
    results = []
    for text in texts:
        try:
            result = check_corpus_safety(text)
            results.append(result)
        except Exception as e:
            results.append({"error": str(e), "text": text})
    return results
