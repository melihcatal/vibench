from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, Optional, Sequence

import requests


OPENAI_MODERATION_API_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


@dataclass(frozen=True)
class OCRSafetyRequest:
    text: str
    model: str = OPENAI_MODERATION_MODEL

    def to_payload(self) -> Dict[str, Any]:
        return {"model": self.model, "input": self.text}


@dataclass(frozen=True)
class OCRSafetyCategoryResult:
    flagged: bool
    score: Optional[float] = None


@dataclass(frozen=True)
class OCRSafetyResponse:
    flagged: bool
    categories: Mapping[str, OCRSafetyCategoryResult] = field(default_factory=dict)
    raw: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class OCRSafetyConfig:
    api_key: Optional[str] = None
    base_url: str = OPENAI_MODERATION_API_URL
    timeout: float = 30.0

    @classmethod
    def from_env(cls) -> "OCRSafetyConfig":
        return cls(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_MODERATION_API_URL", OPENAI_MODERATION_API_URL),
            timeout=float(os.getenv("OPENAI_MODERATION_TIMEOUT", "30")),
        )


class OCRSafetyClient:
    def __init__(self, config: Optional[OCRSafetyConfig] = None) -> None:
        self.config = config or OCRSafetyConfig.from_env()

    def _headers(self) -> Dict[str, str]:
        headers = {"content-type": "application/json"}
        if self.config.api_key:
            headers["authorization"] = f"Bearer {self.config.api_key}"
        return headers

    def check(self, text: str) -> OCRSafetyResponse:
        payload = OCRSafetyRequest(text=text).to_payload()
        response = requests.post(
            self.config.base_url,
            json=payload,
            headers=self._headers(),
            timeout=self.config.timeout,
        )
        response.raise_for_status()
        data = response.json()
        result = (data.get("results") or [{}])[0]
        categories = result.get("category_scores") or {}
        category_flags = result.get("categories") or {}
        normalized_categories = {
            name: OCRSafetyCategoryResult(
                flagged=bool(category_flags.get(name, False)),
                score=categories.get(name),
            )
            for name in set(categories) | set(category_flags)
        }
        return OCRSafetyResponse(
            flagged=bool(result.get("flagged", False)),
            categories=normalized_categories,
            raw=data,
        )


def get_ocr_safety_client(config: Optional[OCRSafetyConfig] = None) -> OCRSafetyClient:
    return OCRSafetyClient(config=config)
