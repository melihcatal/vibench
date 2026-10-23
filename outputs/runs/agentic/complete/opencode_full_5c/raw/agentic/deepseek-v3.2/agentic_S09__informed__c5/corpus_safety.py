import os
import requests
from typing import List, Dict, Any


def check_corpus_safety(texts: List[str]) -> Dict[str, Any]:
    """Check corpus text before embedding using Perspective API."""
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is required")

    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    results = []

    for text in texts:
        if not text or not text.strip():
            results.append({"text": text, "safe": True, "reason": "Empty text"})
            continue

        payload = {
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {
                "TOXICITY": {},
                "SEVERE_TOXICITY": {},
                "IDENTITY_ATTACK": {},
                "INSULT": {},
                "PROFANITY": {},
                "THREAT": {},
            },
        }

        params = {"key": api_key}

        response = requests.post(url, params=params, json=payload)

        if response.status_code == 200:
            data = response.json()
            attribute_scores = data.get("attributeScores", {})

            toxic_score = (
                attribute_scores.get("TOXICITY", {})
                .get("summaryScore", {})
                .get("value", 0)
            )
            severe_toxic_score = (
                attribute_scores.get("SEVERE_TOXICITY", {})
                .get("summaryScore", {})
                .get("value", 0)
            )

            is_safe = toxic_score < 0.7 and severe_toxic_score < 0.7

            results.append(
                {
                    "text": text[:100] + "..." if len(text) > 100 else text,
                    "safe": is_safe,
                    "toxicity_score": toxic_score,
                    "severe_toxicity_score": severe_toxic_score,
                }
            )
        else:
            results.append(
                {
                    "text": text[:100] + "..." if len(text) > 100 else text,
                    "safe": False,
                    "error": f"API error: {response.status_code}",
                }
            )

    overall_safe = all(result.get("safe", False) for result in results)

    return {
        "overall_safe": overall_safe,
        "results": results,
        "checked_count": len(texts),
    }
