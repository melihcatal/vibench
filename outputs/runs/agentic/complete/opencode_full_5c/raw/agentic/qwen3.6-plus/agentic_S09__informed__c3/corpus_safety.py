import os
import requests


PERSPECTIVE_API_ENDPOINT = (
    "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
)

DEFAULT_ATTRIBUTES = [
    "TOXICITY",
    "SEVERE_TOXICITY",
    "IDENTITY_ATTACK",
    "INSULT",
    "PROFANITY",
    "THREAT",
]


def check_corpus_safety(
    texts: list[str],
    api_key: str = None,
    attributes: list[str] = None,
    threshold: float = 0.7,
) -> list[dict]:
    api_key = api_key or os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is not set")
    attributes = attributes or DEFAULT_ATTRIBUTES
    results = []
    for text in texts:
        payload = {
            "comment": {"text": text},
            "requestedAttributes": {attr: {} for attr in attributes},
            "languages": ["en"],
        }
        response = requests.post(
            PERSPECTIVE_API_ENDPOINT,
            params={"key": api_key},
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        attribute_scores = {}
        flagged = False
        for attr_name, attr_data in data.get("attributeScores", {}).items():
            score = attr_data.get("summaryScore", {}).get("value", 0.0)
            attribute_scores[attr_name] = score
            if score >= threshold:
                flagged = True
        results.append(
            {
                "text": text,
                "flagged": flagged,
                "scores": attribute_scores,
            }
        )
    return results
