from typing import Dict, Any
import os
import requests


def platform_output_safety(text: str) -> Dict[str, Any]:
    """
    Checks text for unsafe content using Perspective API.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

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
        "languages": ["en"],
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        result = response.json()

        return {
            "provider": "perspective_api",
            "attributes": {
                attr: result["attributeScores"][attr]["summaryScore"]["value"]
                for attr in payload["requestedAttributes"].keys()
            },
            "is_safe": all(
                result["attributeScores"][attr]["summaryScore"]["value"] < 0.7
                for attr in payload["requestedAttributes"].keys()
            ),
        }
    except Exception as e:
        raise RuntimeError(f"Perspective API request failed: {str(e)}")
