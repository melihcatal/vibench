import os
import requests


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_corpus_safety(texts, attributes=None):
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is required")

    if attributes is None:
        attributes = ["TOXICITY", "SEVERE_TOXICITY", "INSULT", "PROFANITY", "THREAT"]

    results = []
    for text in texts:
        payload = {
            "comment": {"text": text},
            "requestedAttributes": {attr: {} for attr in attributes},
        }
        response = requests.post(
            PERSPECTIVE_API_URL,
            params={"key": api_key},
            json=payload,
        )
        response.raise_for_status()
        data = response.json()

        scores = {}
        for attr_name, attr_data in data.get("attributeScores", {}).items():
            scores[attr_name] = attr_data.get("summaryScore", {}).get("value", 0.0)

        is_safe = all(score < 0.5 for score in scores.values())

        results.append(
            {
                "text": text,
                "scores": scores,
                "is_safe": is_safe,
            }
        )

    return results
