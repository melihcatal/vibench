import os
import requests
from typing import List, Dict, Any, Optional


def check_corpus_safety(texts: List[str]) -> List[Dict[str, Any]]:
    """
    Check corpus text for safety using Perspective API.

    Args:
        texts: List of text strings to check

    Returns:
        List[Dict[str, Any]]: Safety analysis results for each text
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is required")

    results = []

    for text in texts:
        if not text.strip():
            results.append(
                {"text": text, "safe": True, "error": "Empty text", "scores": {}}
            )
            continue

        try:
            response = requests.post(
                "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
                params={"key": api_key},
                json={
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
                },
                timeout=10,
            )
            response.raise_for_status()

            data = response.json()
            attribute_scores = data.get("attributeScores", {})

            scores = {}
            for attr_name, attr_data in attribute_scores.items():
                scores[attr_name] = attr_data.get("summaryScore", {}).get("value", 0)

            # Consider text unsafe if any score exceeds threshold
            toxic_score = scores.get("TOXICITY", 0)
            severe_toxic_score = scores.get("SEVERE_TOXICITY", 0)
            identity_attack_score = scores.get("IDENTITY_ATTACK", 0)

            is_safe = (
                toxic_score < 0.7
                and severe_toxic_score < 0.7
                and identity_attack_score < 0.7
            )

            results.append(
                {"text": text, "safe": is_safe, "scores": scores, "error": None}
            )

        except Exception as e:
            results.append({"text": text, "safe": False, "scores": {}, "error": str(e)})

    return results
