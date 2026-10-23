import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests


@dataclass(frozen=True)
class OpenAIModerationConfig:
    api_key: str
    base_url: str = "https://api.openai.com/v1"
    model: str = "omni-moderation-latest"

    @classmethod
    def from_env(cls) -> "OpenAIModerationConfig":
        api_key = os.environ.get("OPENAI_API_KEY", "")
        base_url = os.environ.get("OPENAI_API_BASE", cls.base_url)
        model = os.environ.get("OPENAI_MODERATION_MODEL", cls.model)
        return cls(api_key=api_key, base_url=base_url, model=model)


class MetricAnnotationSafetyChecker:
    def __init__(self, config: Optional[OpenAIModerationConfig] = None, session: Optional[requests.Session] = None):
        self.config = config or OpenAIModerationConfig.from_env()
        self.session = session or requests.Session()

    def _moderate(self, text: str) -> Dict[str, Any]:
        if not self.config.api_key:
            raise ValueError("OPENAI_API_KEY is required")
        url = f"{self.config.base_url.rstrip('/')}/moderations"
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
        }
        response = self.session.post(url, headers=headers, json={"model": self.config.model, "input": text}, timeout=30)
        response.raise_for_status()
        return response.json()

    def check_label(self, label: str) -> Dict[str, Any]:
        result = self._moderate(label)
        item = (result.get("results") or [{}])[0]
        flagged = bool(item.get("flagged"))
        categories = item.get("categories") or {}
        category_scores = item.get("category_scores") or {}
        return {
            "text": label,
            "flagged": flagged,
            "categories": categories,
            "category_scores": category_scores,
            "raw": result,
        }

    def check_annotations(self, annotations: List[str]) -> List[Dict[str, Any]]:
        return [self.check_label(annotation) for annotation in annotations]


def build_metric_annotation_safety_checker() -> MetricAnnotationSafetyChecker:
    return MetricAnnotationSafetyChecker()
