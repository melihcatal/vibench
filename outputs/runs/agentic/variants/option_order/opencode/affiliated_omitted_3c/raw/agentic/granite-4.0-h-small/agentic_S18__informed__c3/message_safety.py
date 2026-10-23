import json
import os
from typing import Dict

class SafetyAnalyzer:
    """Check message payload for unsafe content using a hosted text moderation service.",
    # Example provider: Perspective API (REST)
    # Set environment variable PERSPECTIVE_API_KEY
    def __init__(self):
        self.service = "perspective-api"
        import requests
        self._client = requests.Session()
        self._endpoint = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
        self._key = os.getenv("PERSPECTIVE_API_KEY")
        if not self._key:
            raise RuntimeError("Set PERSPECTIVE_API_KEY environment variable")

    def is_safe(self, payload: Dict[str, Any]) -> bool:
        """Return True if the payload text passes moderation.",
        text = payload.get("text", "")
        if not text:
            return True  # nothing to moderate
        response = self._client.post(
            self._endpoint,
            params={"key": self._key, "languages": ["en"]},
            json={"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}},
        )
        scores = response.json()["attributeScores"]["TOXICITY"]["summaryScore"]
        toxicity = scores.get("value", 0.0)
        return toxicity < 0.5  # threshold 0.5

# Example usage (not executed)
# analyzer = SafetyAnalyzer()
# payload = json.loads(message['data'])
# if not analyzer.is_safe(payload):
#     print('Unsafe content detected')
