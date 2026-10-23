from __future__ import annotations

import os
from typing import Dict, Iterable, List, Optional

import requests

from safety_models import SafetyRequest


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
PERSPECTIVE_DEFAULT_ATTRIBUTES: List[str] = [
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
        requested_attributes: Optional[Iterable[str]] = None,
        do_not_store: bool = True,
    ) -> None:
        self.api_key = api_key or os.environ["PERSPECTIVE_API_KEY"]
        self.session = session or requests.Session()
        self.requested_attributes = list(requested_attributes or PERSPECTIVE_DEFAULT_ATTRIBUTES)
        self.do_not_store = do_not_store

    def build_payload(self, request: SafetyRequest) -> Dict[str, object]:
        payload: Dict[str, object] = {
            "comment": {"text": request.text},
            "requestedAttributes": {name: {} for name in self.requested_attributes},
            "doNotStore": self.do_not_store,
        }
        if request.language:
            payload["languages"] = [request.language]
        return payload

    def analyze(self, request: SafetyRequest) -> Dict[str, object]:
        response = self.session.post(
            PERSPECTIVE_API_URL,
            params={"key": self.api_key},
            json=self.build_payload(request),
            timeout=30,
        )
        response.raise_for_status()
        return response.json()
