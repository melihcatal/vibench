from typing import Dict, List, Optional
import os
import requests


def check_secret_labels_for_unsafe_text(
    secret_name: str, labels: Dict[str, str]
) -> Dict[str, Any]:
    """
    Checks secret labels and notes for unsafe text using Perspective API.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("Perspective API key not configured.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    results = {}

    for label_key, label_value in labels.items():
        payload = {
            "comment": {"text": label_value},
            "requestedAttributes": {
                "TOXICITY": {},
                "SEVERE_TOXICITY": {},
                "IDENTITY_ATTACK": {},
                "INSULT": {},
                "PROFANITY": {},
                "THREAT": {},
            },
            "languages": ["en"],
        }

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            analysis = response.json()

            results[label_key] = {
                "unsafe": any(
                    analysis.get("attributeScores", {})
                    .get(attr, {})
                    .get("summaryScore", {})
                    .get("value", 0)
                    > 0.7
                    for attr in [
                        "TOXICITY",
                        "SEVERE_TOXICITY",
                        "IDENTITY_ATTACK",
                        "INSULT",
                        "PROFANITY",
                        "THREAT",
                    ]
                ),
                "scores": {
                    attr: analysis.get("attributeScores", {})
                    .get(attr, {})
                    .get("summaryScore", {})
                    .get("value", 0)
                    for attr in [
                        "TOXICITY",
                        "SEVERE_TOXICITY",
                        "IDENTITY_ATTACK",
                        "INSULT",
                        "PROFANITY",
                        "THREAT",
                    ]
                },
            }
        except Exception as e:
            print(f"Failed to analyze label {label_key}: {e}")
            results[label_key] = {"unsafe": False, "error": str(e)}

    return {
        "secret_name": secret_name,
        "labels_checked": list(labels.keys()),
        "unsafe_labels": [k for k, v in results.items() if v.get("unsafe", False)],
        "details": results,
    }
