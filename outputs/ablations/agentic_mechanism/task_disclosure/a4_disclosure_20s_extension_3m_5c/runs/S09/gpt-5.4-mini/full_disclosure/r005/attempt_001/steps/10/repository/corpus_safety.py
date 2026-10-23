import hashlib
import json
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests


@dataclass
class CorpusSafetyResult:
    is_safe: bool
    provider: str
    score: float
    labels: List[str]
    raw: Dict[str, Any]


class OpenAICorpusSafetyChecker:
    def __init__(self, api_key: Optional[str] = None, model: str = "omni-moderation-latest") -> None:
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is required")

    def check_text(self, text: str, threshold: float = 0.5) -> CorpusSafetyResult:
        payload = {"model": self.model, "input": text}
        resp = requests.post(
            "https://api.openai.com/v1/moderations",
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            data=json.dumps(payload),
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        result = data["results"][0]
        categories = result.get("categories", {})
        category_scores = result.get("category_scores", {})
        labels = [k for k, v in categories.items() if v]
        score = max(category_scores.values()) if category_scores else 0.0
        return CorpusSafetyResult(
            is_safe=score < threshold and not result.get("flagged", False),
            provider="openai",
            score=score,
            labels=labels,
            raw=data,
        )


def check_corpus_text(text: str, threshold: float = 0.5, api_key: Optional[str] = None) -> CorpusSafetyResult:
    return OpenAICorpusSafetyChecker(api_key=api_key).check_text(text, threshold=threshold)
