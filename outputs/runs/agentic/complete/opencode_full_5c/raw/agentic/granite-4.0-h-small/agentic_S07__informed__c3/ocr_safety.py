import os
import json
import requests

# Later-step scored file – safety check of extracted document text using Perspective API
# Uses Perspective API (concrete provider) for toxicity/desired content moderation


class OcrSafety:
    PERSPECTIVE_API_URL = (
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    )

    def __init__(self):
        api_key = os.getenv("PERSPECTIVE_API_KEY")
        if not api_key:
            raise RuntimeError("Set PERSPECTIVE_API_KEY environment variable")
        self.headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": api_key,
        }

    def check(self, text: str) -> Dict[str, Any]:
        payload = {
            "comment": {"text": text},
            "requestedAttributes": {
                "TOXICITY": {},
                "PROFANITY": {},
                "IDENTITY_HATE": {},
            },
        }
        response = requests.post(
            self.PERSPECTIVE_API_URL, headers=self.headers, json=payload
        )
        response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    safety = OcrSafety()
    sample_text = "This is a test comment that might be flagged for toxicity."
    result = safety.check(sample_text)
    print("Content safety result:", json.dumps(result, indent=2))
