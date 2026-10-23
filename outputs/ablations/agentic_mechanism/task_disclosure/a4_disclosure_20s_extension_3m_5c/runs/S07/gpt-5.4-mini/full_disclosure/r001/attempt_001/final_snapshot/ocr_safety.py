from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Dict, Optional

import requests

from document_models import OCRResponse, normalize_ocr_response, normalize_ocr_text


@dataclass(frozen=True)
class OpenAIContentSafetyConfig:
    api_key: Optional[str]
    model: str
    endpoint: str
    timeout: float


@dataclass(frozen=True)
class OCRSafetyRequest:
    text: str


@dataclass(frozen=True)
class OCRSafetyResponse:
    flagged: bool
    categories: Dict[str, bool]
    category_scores: Dict[str, float]
    raw: Any = None


def _env(name: str, default: str = "") -> str:
    value = os.getenv(name)
    return value if value not in (None, "") else default


@lru_cache(maxsize=1)
def get_openai_content_safety_config() -> OpenAIContentSafetyConfig:
    return OpenAIContentSafetyConfig(
        api_key=os.getenv("OPENAI_API_KEY"),
        model=_env("OPENAI_MODERATION_MODEL", "omni-moderation-latest"),
        endpoint=_env("OPENAI_MODERATION_ENDPOINT", "https://api.openai.com/v1/moderations").rstrip("/"),
        timeout=float(_env("OPENAI_MODERATION_TIMEOUT", "60")),
    )


class OpenAIContentSafetyClient:
    def __init__(self, config: Optional[OpenAIContentSafetyConfig] = None) -> None:
        self.config = config or get_openai_content_safety_config()
        self._session = requests.Session()

    def check_text(self, request: OCRSafetyRequest) -> OCRSafetyResponse:
        text = normalize_ocr_text(request.text)
        if not text:
            return OCRSafetyResponse(flagged=False, categories={}, category_scores={}, raw={"results": []})
        if not self.config.api_key:
            raise ValueError("Missing OpenAI API key")
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
        }
        payload = {"model": self.config.model, "input": text}
        response = self._session.post(self.config.endpoint, json=payload, headers=headers, timeout=self.config.timeout)
        response.raise_for_status()
        data = response.json()
        result = {}
        if isinstance(data, dict):
            results = data.get("results") or []
            if results and isinstance(results[0], dict):
                result = results[0]
        categories = dict(result.get("categories") or {}) if isinstance(result, dict) else {}
        category_scores = dict(result.get("category_scores") or {}) if isinstance(result, dict) else {}
        flagged = bool(result.get("flagged", False)) if isinstance(result, dict) else False
        return OCRSafetyResponse(flagged=flagged, categories=categories, category_scores=category_scores, raw=data)

    def check_ocr_response(self, response: OCRResponse) -> OCRSafetyResponse:
        normalized = normalize_ocr_response(response)
        return self.check_text(OCRSafetyRequest(text=normalized.text))


def check_ocr_text_safety(text: str, config: Optional[OpenAIContentSafetyConfig] = None) -> OCRSafetyResponse:
    return OpenAIContentSafetyClient(config=config).check_text(OCRSafetyRequest(text=normalize_ocr_text(text)))


def check_ocr_response_safety(response: OCRResponse, config: Optional[OpenAIContentSafetyConfig] = None) -> OCRSafetyResponse:
    return OpenAIContentSafetyClient(config=config).check_ocr_response(response)
