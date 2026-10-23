import os
import requests
from typing import List, Dict, Any


def check_corpus_safety(texts: List[str]) -> List[Dict[str, Any]]:
    """Check corpus text before embedding using Perspective API."""
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is required")

    results = []
    base_url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    for text in texts:
        if not text or not text.strip():
            results.append({"text": text, "safe": True, "reasons": ["empty"]})
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

        try:
            response = requests.post(
                f"{base_url}?key={api_key}", json=payload, timeout=10
            )
            response.raise_for_status()

            data = response.json()
            attribute_scores = data.get("attributeScores", {})

            is_safe = True
            reasons = []

            for attr_name, attr_data in attribute_scores.items():
                score = attr_data.get("summaryScore", {}).get("value", 0)
                if score > 0.7:
                    is_safe = False
                    reasons.append(f"{attr_name.lower()}:{score:.2f}")

            results.append(
                {
                    "text": text[:100] + "..." if len(text) > 100 else text,
                    "safe": is_safe,
                    "reasons": reasons if not is_safe else ["safe"],
                }
            )

        except Exception as e:
            results.append(
                {
                    "text": text[:100] + "..." if len(text) > 100 else text,
                    "safe": False,
                    "reasons": [f"error: {str(e)}"],
                }
            )

    return results
