from typing import List
import requests

def unsafe_copy_check(texts: List[str], lang: str) -> List[bool]:
    """Check localized copy for unsafe content using Perspective API."""
    api_key = "PERSPECTIVE_API_KEY"
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    results = []

    for text in texts:
        payload = {
            "comment": {"text": text, "language": lang},
            "requestedAttributes": {
                "TOXICITY": {},
                "SEVERE_TOXICITY": {},
                "IDENTITY_ATTACK": {},
                "INSULT": {},
                "PROFANITY": {},
            },
            "languages": [lang],
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()
        attribute_scores = response.json().get("attributeScores", {})
        is_unsafe = any(
            score["summaryScore"]["value"] > 0.7
            for score in attribute_scores.values()
        )
        results.append(is_unsafe)

    return results