import os
import requests
from typing import List, Dict, Any


def check_corpus_safety(texts: List[str]) -> Dict[str, Any]:
    """
    Check corpus text for safety before embedding using Google Perspective API.

    Args:
        texts: List of text strings to check

    Returns:
        Dictionary with safety analysis results
    """
    api_key = os.getenv("GOOGLE_PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_PERSPECTIVE_API_KEY environment variable is required")

    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    results = {
        "total_texts": len(texts),
        "unsafe_texts": 0,
        "safety_scores": [],
        "details": [],
    }

    for text in texts:
        if len(text) > 2048:
            text = text[:2048]

        params = {"key": api_key}

        data = {
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

        try:
            response = requests.post(url, params=params, json=data)
            response.raise_for_status()
            analysis = response.json()

            attribute_scores = analysis.get("attributeScores", {})
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

            is_unsafe = toxicity_score > 0.7 or severe_toxicity_score > 0.7

            if is_unsafe:
                results["unsafe_texts"] += 1

            results["safety_scores"].append(
                {
                    "text_preview": text[:100] + "..." if len(text) > 100 else text,
                    "toxicity": toxicity_score,
                    "severe_toxicity": severe_toxicity_score,
                    "is_unsafe": is_unsafe,
                }
            )

            results["details"].append(analysis)

        except Exception as e:
            results["safety_scores"].append(
                {
                    "text_preview": text[:100] + "..." if len(text) > 100 else text,
                    "error": str(e),
                    "is_unsafe": False,
                }
            )

    return results
