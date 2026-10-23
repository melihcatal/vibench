import os
from typing import Any, Dict, List, Optional

import requests

from safety_models import SafetyDecision, SafetyRequest, normalize_text


class TisaneSafetyClient:
    base_url = "https://api.tisane.ai/parse"

    def __init__(
        self, api_key: Optional[str] = None, session: Optional[requests.Session] = None
    ):
        self.api_key = api_key or os.environ.get("TISANE_API_KEY")
        self.session = session or requests.Session()

    def _headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["X-Api-Key"] = self.api_key
        return headers

    def moderate(self, text: str, language: str = "en") -> SafetyDecision:
        payload = {"content": normalize_text(text), "language": language}
        response = self.session.post(
            self.base_url, json=payload, headers=self._headers(), timeout=30
        )
        response.raise_for_status()
        data = response.json()
        scores = {
            "toxicity": float(data.get("toxicity", 0.0)),
            "hate": float(data.get("hate", 0.0)),
            "sexual": float(data.get("sexual", 0.0)),
            "violence": float(data.get("violence", 0.0)),
        }
        allowed = not any(v >= 0.5 for v in scores.values())
        return SafetyDecision(
            allowed=allowed,
            categories=scores,
            rationale=data.get("summary"),
            provider_response=data,
        )

    def moderate_request(self, request: SafetyRequest) -> SafetyDecision:
        return self.moderate(request.text, language=request.language or "en")

    def redact_spans(self, text: str, spans: List[Dict[str, Any]]) -> str:
        chars = list(text)
        for span in spans:
            start = max(0, int(span.get("start", 0)))
            end = min(len(chars), int(span.get("end", 0)))
            for i in range(start, end):
                chars[i] = "█"
        return "".join(chars)
