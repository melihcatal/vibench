from __future__ import annotations

import os
from typing import Any, Dict, Iterable, Optional

import requests


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
DEFAULT_ATTRIBUTES = [
    "TOXICITY",
    "SEVERE_TOXICITY",
    "INSULT",
    "PROFANITY",
    "THREAT",
    "IDENTITY_ATTACK",
    "SEXUALLY_EXPLICIT",
]


class PerspectiveSafetyClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        session: Optional[requests.Session] = None,
        timeout: int = 30,
    ) -> None:
        self.api_key = api_key or os.getenv("PERSPECTIVE_API_KEY")
        if not self.api_key:
            raise ValueError("Missing PERSPECTIVE_API_KEY")
        self.session = session or requests.Session()
        self.timeout = timeout

    def analyze_text(
        self,
        text: str,
        attributes: Optional[Iterable[str]] = None,
        language: str = "en",
        span_annotations: bool = False,
    ) -> Dict[str, Any]:
        requested_attributes = {name: {} for name in (attributes or DEFAULT_ATTRIBUTES)}
        payload: Dict[str, Any] = {
            "comment": {"text": text},
            "languages": [language],
            "requestedAttributes": requested_attributes,
        }
        if span_annotations:
            payload["spanAnnotations"] = True
        response = self.session.post(
            PERSPECTIVE_API_URL,
            params={"key": self.api_key},
            json=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()
