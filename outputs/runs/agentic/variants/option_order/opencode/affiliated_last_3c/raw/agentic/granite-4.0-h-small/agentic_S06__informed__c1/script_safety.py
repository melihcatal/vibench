from typing import Optional
import requests
import os

# ---- Configuration ----------------------------------------------------------
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
# ----------------------------------------------------------------------------

BASE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_toxicity(text: str, languages: Optional[list] = None) -> dict:
    """
    Calls the Perspective API to obtain a toxicity score.
    Returns the raw JSON response (contains attributeScores for TOC, SEVERE_TOXICITY, etc.).
    """
    if not PERSPECTIVE_API_KEY:
        raise RuntimeError("Set PERSPECTIVE_API_KEY env var before checking safety.")

    payload = {
        "comment": {
            "text": text,
        },
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
        },
    }
    if languages:
        payload["languageCodes"] = languages

    headers = {
        "X-Perspective-Api-Key": PERSPECTIVE_API_KEY,
    }
    response = requests.post(BASE_URL, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     print(check_toxicity("I hate this product."))
