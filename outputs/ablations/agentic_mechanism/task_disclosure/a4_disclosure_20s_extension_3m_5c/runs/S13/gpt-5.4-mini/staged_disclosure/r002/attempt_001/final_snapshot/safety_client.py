import os
from typing import Any, Dict, Mapping, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"
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


class SafetyClient:
    def __init__(self, api_key: Optional[str] = None, thresholds: Optional[Mapping[str, float]] = None) -> None:
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.thresholds = dict(DEFAULT_CATEGORY_THRESHOLDS)
        if thresholds:
            self.thresholds.update(thresholds)

    def score_text(self, text: str) -> Dict[str, Any]:
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY is required")
        response = requests.post(
            OPENAI_MODERATION_URL,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={"model": OPENAI_MODERATION_MODEL, "input": text},
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        result = (data.get("results") or [{}])[0]
        return {
            "flagged": bool(result.get("flagged", False)),
            "categories": result.get("categories", {}),
            "category_scores": result.get("category_scores", {}),
            "raw": data,
        }

    def allow_text(self, text: str) -> bool:
        scores = self.score_text(text).get("category_scores", {})
        for category, threshold in self.thresholds.items():
            if scores.get(category, 0.0) >= threshold:
                return False
        return True


def build_safety_client(api_key: Optional[str] = None, thresholds: Optional[Mapping[str, float]] = None) -> SafetyClient:
    return SafetyClient(api_key=api_key, thresholds=thresholds)


def score_text(text: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    return build_safety_client(api_key=api_key).score_text(text)


def allow_text(text: str, api_key: Optional[str] = None, thresholds: Optional[Mapping[str, float]] = None) -> bool:
    return build_safety_client(api_key=api_key, thresholds=thresholds).allow_text(text)
