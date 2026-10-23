import os
import requests
from document_client import DocumentClient
from document_models import SafetyCheckRequest, SafetyCheckResponse


class SafetyChecker:
    def __init__(self):
        # Perspective API authentication via environment variable
        self.api_key = os.getenv("PERSPECTIVE_API_KEY")
        self.client = DocumentClient()
        self.endpoint = (
            "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
        )

    def check(self, text: str, attribute: str = "TOXICITY") -> SafetyCheckResponse:
        """Check extracted document text for unsafe content using Perspective API.

        Args:
            text: Text to be evaluated.
            attribute: Toxicity attribute to check (default 'TOXICITY').

        Returns:
            SafetyCheckResponse containing the toxicity score.
        """
        payload = {
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {attribute: {}},
        }
        headers = {"content-type": "application/json", "x-api-key": self.api_key}
        response = requests.post(self.endpoint, json=payload, headers=headers)
        result = response.json()["attributeScores"][attribute]["summaryScore"]["value"]
        return SafetyCheckResponse(toxicity_score=result)


if __name__ == "__main__":
    checker = SafetyChecker()
    result = checker.check("Sample text with offensive language.")
    print(result.toxicity_score)
