import os
import requests
from typing import List, Dict, Any

# Perspective API endpoint and key
PERSPECTIVE_API_BASE_URL = (
    "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
)


def check_text_safety(texts: List[str]) -> Dict[str, Dict[str, Any]]:
    perspective_api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not perspective_api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    results = {}
    for i, text in enumerate(texts):
        if not text.strip():
            results[f"text_{i}"] = {"error": "Empty text provided"}
            continue

        request_body = {
            "comment": {"text": text},
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
                f"{PERSPECTIVE_API_BASE_URL}?key={perspective_api_key}",
                json=request_body,
            )
            response.raise_for_status()  # Raise an exception for HTTP errors
            analysis_result = response.json()

            # Extract scores, default to 0 if attribute not found
            scores = {
                attr: analysis_result.get("attributeScores", {})
                .get(attr, {})
                .get("summaryScore", {})
                .get("value", 0.0)
                for attr in [
                    "TOXICITY",
                    "SEVERE_TOXICITY",
                    "IDENTITY_ATTACK",
                    "INSULT",
                    "PROFANITY",
                    "THREAT",
                ]
            }
            results[f"text_{i}"] = scores
        except requests.exceptions.RequestException as e:
            results[f"text_{i}"] = {"error": str(e)}

    return results
