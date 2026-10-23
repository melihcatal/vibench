import os
from typing import Dict, Any
import requests
from pydantic import BaseModel


class ModerationRequest(BaseModel):
    text: str
    language: str = "en"


class ModerationResponse(BaseModel):
    is_flagged: bool
    categories: Dict[str, bool]
    scores: Dict[str, float]


class PerspectiveAPIClient:
    def __init__(self):
        self.api_key = os.getenv("PERSPECTIVE_API_KEY")
        self.url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    def moderate_text(self, request: ModerationRequest) -> ModerationResponse:
        response = requests.post(
            self.url,
            params={"key": self.api_key},
            json={
                "comment": {"text": request.text},
                "languages": [request.language],
                "requestedAttributes": {
                    "TOXICITY": {},
                    "SEVERE_TOXICITY": {},
                    "IDENTITY_ATTACK": {},
                    "INSULT": {},
                    "PROFANITY": {},
                    "THREAT": {},
                },
            },
        )
        response.raise_for_status()
        result = response.json()
        attribute_scores = result.get("attributeScores", {})

        return ModerationResponse(
            is_flagged=any(
                attribute_scores.get(attr, {}).get("summaryScore", {}).get("value", 0)
                > 0.7
                for attr in attribute_scores
            ),
            categories={
                attr: attribute_scores.get(attr, {})
                .get("summaryScore", {})
                .get("value", 0)
                > 0.7
                for attr in attribute_scores
            },
            scores={
                attr: attribute_scores.get(attr, {})
                .get("summaryScore", {})
                .get("value", 0)
                for attr in attribute_scores
            },
        )


def profile_moderation(text: str) -> ModerationResponse:
    client = PerspectiveAPIClient()
    request = ModerationRequest(text=text)
    return client.moderate_text(request)
