from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests


PERSPECTIVE_API_HOST = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
PERSPECTIVE_MODEL = "commentanalyzer-v1alpha1"

DEFAULT_ATTRIBUTES = [
    "TOXICITY",
    "SEVERE_TOXICITY",
    "INSULT",
    "THREAT",
    "PROFANITY",
    "IDENTITY_ATTACK",
    "SEXUALLY_EXPLICIT",
]


class PerspectiveSafetyClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        session: Optional[requests.Session] = None,
        timeout: float = 20.0,
    ) -> None:
        self.api_key = api_key or os.environ["PERSPECTIVE_API_KEY"]
        self.session = session or requests.Session()
        self.timeout = timeout
        self.endpoint = PERSPECTIVE_API_HOST
        self.model = PERSPECTIVE_MODEL

    def analyze_text(
        self,
        text: str,
        attributes: Optional[list[str]] = None,
        language: str = "en",
        do_not_store: bool = True,
    ) -> Dict[str, Any]:
        requested_attributes = {
            name: {} for name in (attributes or DEFAULT_ATTRIBUTES)
        }
        payload = {
            "comment": {"text": text},
            "languages": [language],
            "requestedAttributes": requested_attributes,
            "doNotStore": do_not_store,
        }
        response = self.session.post(
            self.endpoint,
            params={"key": self.api_key},
            json=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()


def extract_attribute_scores(response_json: Dict[str, Any]) -> Dict[str, float]:
    scores: Dict[str, float] = {}
    for name, detail in response_json.get("attributeScores", {}).items():
        value = (
            detail.get("summaryScore", {})
            .get("value", 0.0)
        )
        scores[name] = float(value)
    return scores
