import requests
import json
import os

def moderate_batch_messages(messages: list[str]) -> list[dict]:
    """
    Moderates a batch of user messages using Google's Perspective API
    and returns per-message decisions.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    api_url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    decisions = []

    for message in messages:
        payload = {
            "comment": {
                "text": message
            },
            "requestedAttributes": {
                "TOXICITY": {},
                "PROFANITY": {},
                "FLIRTATION": {}
            },
            "languages": ["en"]
        }

        headers = {
            "Content-Type": "application/json"
        }

        params = {
            "key": api_key
        }

        try:
            response = requests.post(api_url, headers=headers, params=params, data=json.dumps(payload))
            response.raise_for_status()
            result = response.json()
            decisions.append({
                "message": message,
                "moderation_scores": result.get("attributeScores", {})
            })
        except requests.exceptions.RequestException as e:
            decisions.append({
                "message": message,
                "error": str(e),
                "moderation_scores": {}
            })
    return decisions