import os
from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
DEFAULT_MODERATION_MODEL = "omni-moderation-latest"


@dataclass(frozen=True)
class SafetyConfig:
    api_key: str
    model: str = DEFAULT_MODERATION_MODEL
    timeout: int = 30


def load_safety_config(api_key: Optional[str] = None, model: Optional[str] = None, timeout: Optional[int] = None) -> SafetyConfig:
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")
    return SafetyConfig(api_key=key, model=model or os.getenv("OPENAI_MODERATION_MODEL", DEFAULT_MODERATION_MODEL), timeout=timeout or int(os.getenv("OPENAI_MODERATION_TIMEOUT", "30")))


class SafetyClient:
    def __init__(self, config: Optional[SafetyConfig] = None) -> None:
        self.config = config or load_safety_config()

    def moderate_text(self, text: str) -> Dict[str, Any]:
        response = requests.post(
            OPENAI_MODERATION_URL,
            headers={
                "Authorization": f"Bearer {self.config.api_key}",
                "Content-Type": "application/json",
            },
            json={"model": self.config.model, "input": text},
            timeout=self.config.timeout,
        )
        response.raise_for_status()
        return response.json()

    def allow_text(self, text: str, thresholds: Mapping[str, float]) -> bool:
        data = self.moderate_text(text)
        results = data.get("results", [])
        if not results:
            return False
        scores: Dict[str, float] = results[0].get("category_scores", {})
        for category, threshold in thresholds.items():
            if float(scores.get(category, 0.0)) >= float(threshold):
                return False
        return True


def get_safety_client(api_key: Optional[str] = None, model: Optional[str] = None, timeout: Optional[int] = None) -> SafetyClient:
    return SafetyClient(load_safety_config(api_key=api_key, model=model, timeout=timeout))


def moderate_text(text: str, api_key: Optional[str] = None, model: Optional[str] = None, timeout: Optional[int] = None) -> Dict[str, Any]:
    return get_safety_client(api_key=api_key, model=model, timeout=timeout).moderate_text(text)


def allow_text(text: str, thresholds: Mapping[str, float], api_key: Optional[str] = None, model: Optional[str] = None, timeout: Optional[int] = None) -> bool:
    return get_safety_client(api_key=api_key, model=model, timeout=timeout).allow_text(text, thresholds)
