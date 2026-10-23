import requests
from translation_client import TranslationClient
from translation_models import TranslationRequest, TranslationResponse


class PerspectiveClient:
    """Client to call Perspective API for translation content safety."""

    def __init__(self):
        api_key = os.getenv("PERSPECTIVE_API_KEY")
        if not api_key:
            raise RuntimeError("PERSPECTIVE_API_KEY not set")
        self.headers = {"key": api_key}
        self.endpoint = (
            "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
        )

    def assess(self, translated_text: str) -> dict:
        payload = {
            "comment": {"text": translated_text},
            "languages": ["en"],
            "attributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}},
        }
        resp = requests.post(self.endpoint, json=payload, headers=self.headers)
        resp.raise_for_status()
        attr = resp.json()["attributeScores"]
        return {
            "toxicity": attr.get("TOXICITY", {}).get("summaryScore", {}).get("value"),
            "severe_toxicity": attr.get("SEVERE_TOXICITY", {})
            .get("summaryScore", {})
            .get("value"),
        }
