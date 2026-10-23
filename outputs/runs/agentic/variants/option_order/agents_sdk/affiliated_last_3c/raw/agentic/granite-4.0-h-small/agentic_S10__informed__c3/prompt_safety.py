# [LATER-STEP] prompt_safety.py

import os
import requests

class PerspectiveModerator:
    """Wrapper around Perspective API for prompt safety checking."""
    BASE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    API_KEY = os.getenv("PERSPECTIVE_API_KEY")
    if not API_KEY:
        raise RuntimeError("Set PERSPECTIVE_API_KEY environment variable")

    @staticmethod
    def check(text: str) -> bool:
        """Return True if the prompt is likely safe, otherwise False."""
        payload = {
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}}
        }
        headers = {"Content-Type": "application/json", "x-api-key": PerspectiveModerator.API_KEY}
        resp = requests.post(PerspectiveModerator.BASE_URL, json=payload, headers=headers)
        resp.raise_for_status()
        result = resp.json()
        # Simple rule: if any severe toxicity score >= 0.5, reject
        severe = result.get("attributeScores", {}).get("SEVERE_TOXICITY", {}).get("summaryScore", {})
        score = severe.get("value", 0.0)
        return score < 0.5
