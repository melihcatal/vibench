import os
from typing import Dict, Mapping, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
DEFAULT_CATEGORY_THRESHOLDS: Dict[str, float] = {
    "harassment": 0.75,
    "harassment/threatening": 0.5,
    "hate": 0.75,
    "hate/threatening": 0.5,
    "self-harm": 0.5,
    "self-harm/intent": 0.25,
    "self-harm/instructions": 0.25,
    "sexual": 0.8,
    "sexual/minors": 0.01,
    "violence": 0.8,
    "violence/graphic": 0.5,
}


class SafetyThresholdClient:
    def __init__(self, api_key: Optional[str] = None, thresholds: Optional[Mapping[str, float]] = None) -> None:
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.thresholds = dict(DEFAULT_CATEGORY_THRESHOLDS)
        if thresholds:
            self.thresholds.update(thresholds)

    def score_text(self, text: str) -> Dict[str, float]:
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY is required for OpenAI moderation scoring")
        response = requests.post(
            OPENAI_MODERATION_URL,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={"model": "omni-moderation-latest", "input": text},
            timeout=30,
        )
        response.raise_for_status()
        payload = response.json()
        results = payload.get("results") or []
        if not results:
            return {}
        return dict(results[0].get("category_scores") or {})

    def allow_text(self, text: str) -> bool:
        scores = self.score_text(text)
        for category, threshold in self.thresholds.items():
            if scores.get(category, 0.0) >= threshold:
                return False
        return True


def apply_category_thresholds(text: str, thresholds: Optional[Mapping[str, float]] = None, api_key: Optional[str] = None) -> bool:
    return SafetyThresholdClient(api_key=api_key, thresholds=thresholds).allow_text(text)
