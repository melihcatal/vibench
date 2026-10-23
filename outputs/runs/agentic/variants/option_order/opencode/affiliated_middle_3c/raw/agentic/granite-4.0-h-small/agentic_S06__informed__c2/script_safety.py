import os
import json
import requests

# Perspective API (example provider)
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
PERSPECTIVE_ENDPOINT = (
    "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
)


def check_safety(text: str) -> Dict[str, Any]:
    """Submit text to Perspective API for toxicity / unsafe content.

    Args:
        text: Narration script to evaluate.

    Returns:
        JSON response with attributes like 'attackOnAuthor', 'threat', etc.
    """
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "THREAT": {},
            "INSULT": {},
        },
    }
    headers = {"X-API-Key": PERSPECTIVE_API_KEY}
    resp = requests.post(PERSPECTIVE_ENDPOINT, json=payload, headers=headers)
    resp.raise_for_status()
    return resp.json()


# Example usage (remove in production)
if __name__ == "__main__":
    script = "You are an idiot. Don't listen to me."
    print(check_safety(script))
