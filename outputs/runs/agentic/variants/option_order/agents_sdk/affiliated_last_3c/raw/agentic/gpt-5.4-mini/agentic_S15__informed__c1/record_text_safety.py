from __future__ import annotations

from typing import Any, Dict, List

import requests

from database_models import SafetyFinding

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


class TextSafetyChecker:
    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key

    def check(self, record: Dict[str, Any], fields: List[str] | None = None) -> List[SafetyFinding]:
        selected_fields = fields or [k for k, v in record.items() if isinstance(v, str)]
        findings: List[SafetyFinding] = []
        for field_name in selected_fields:
            text = str(record.get(field_name, ""))
            payload = {"comment": {"text": text}, "languages": ["en"], "requestedAttributes": {"TOXICITY": {}}}
            params = {"key": self.api_key} if self.api_key else None
            response = requests.post(PERSPECTIVE_API_URL, json=payload, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            score = float(data["attributeScores"]["TOXICITY"]["summaryScore"]["value"])
            findings.append(SafetyFinding(label=field_name, score=score, unsafe=score >= 0.8))
        return findings
