import os
import requests
from typing import Dict, Any
from security_models import SecretMetadata


def check_label_safety(metadata: SecretMetadata) -> Dict[str, Any]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError(
            "PERSPECTIVE_API_KEY environment variable not set for Perspective API."
        )

    api_endpoint = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    results = {}

    text_to_analyze = []
    if metadata.description:
        text_to_analyze.append(metadata.description)
    for key, value in metadata.labels.items():
        text_to_analyze.append(f"{key}: {value}")

    if not text_to_analyze:
        return {"status": "No text to analyze."}

    for text in text_to_analyze:
        payload = {
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
            response = requests.post(f"{api_endpoint}?key={api_key}", json=payload)
            response.raise_for_status()
            analysis_result = response.json()
            results[text] = analysis_result
        except requests.exceptions.RequestException as e:
            results[text] = {"error": f"Perspective API request failed: {e}"}
    return results
