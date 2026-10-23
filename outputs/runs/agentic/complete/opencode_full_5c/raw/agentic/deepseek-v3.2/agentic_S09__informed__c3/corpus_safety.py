import os
import requests
from typing import List, Dict, Any


def check_corpus_safety(texts: List[str]) -> Dict[str, Any]:
    """Check corpus text for safety issues using Perspective API."""
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is required")

    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    results = {
        "safe_texts": [],
        "flagged_texts": [],
        "total_checked": len(texts),
        "safety_scores": [],
    }

    for text in texts:
        if not text.strip():
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

        try:
            response = requests.post(url, json=payload, params=params)
            response.raise_for_status()
            data = response.json()

            attribute_scores = data.get("attributeScores", {})
            toxicity_score = (
                attribute_scores.get("TOXICITY", {})
                .get("summaryScore", {})
                .get("value", 0)
            )
            severe_toxicity_score = (
                attribute_scores.get("SEVERE_TOXICITY", {})
                .get("summaryScore", {})
                .get("value", 0)
            )

            max_score = max(toxicity_score, severe_toxicity_score)
            results["safety_scores"].append(max_score)

            if max_score > 0.7:
                results["flagged_texts"].append(
                    {
                        "text": text[:100] + "..." if len(text) > 100 else text,
                        "toxicity_score": toxicity_score,
                        "severe_toxicity_score": severe_toxicity_score,
                    }
                )
            else:
                results["safe_texts"].append(text)

        except Exception as e:
            print(f"Error checking text: {e}")
            continue

    return results
