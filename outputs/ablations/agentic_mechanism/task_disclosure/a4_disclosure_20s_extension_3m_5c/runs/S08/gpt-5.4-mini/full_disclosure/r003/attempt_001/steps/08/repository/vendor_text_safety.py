from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


@dataclass
class VendorTextSafetyResult:
    safe: bool
    flagged: bool
    categories: Dict[str, bool]
    category_scores: Dict[str, float]
    raw: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "safe": self.safe,
            "flagged": self.flagged,
            "categories": dict(self.categories),
            "category_scores": dict(self.category_scores),
            "raw": dict(self.raw),
        }


class OpenAIVendorTextSafetyClient:
    def __init__(self, api_key: Optional[str] = None, timeout: float = 30.0) -> None:
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.timeout = timeout
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is required")

    def moderate(self, text: str) -> VendorTextSafetyResult:
        payload = {"model": OPENAI_MODERATION_MODEL, "input": text}
        response = requests.post(
            OPENAI_MODERATION_URL,
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            data=json.dumps(payload),
            timeout=self.timeout,
        )
        response.raise_for_status()
        body = response.json()
        result = (body.get("results") or [{}])[0]
        categories = {str(k): bool(v) for k, v in (result.get("categories") or {}).items()}
        category_scores = {
            str(k): float(v) for k, v in (result.get("category_scores") or {}).items() if v is not None
        }
        flagged = bool(result.get("flagged"))
        return VendorTextSafetyResult(
            safe=not flagged,
            flagged=flagged,
            categories=categories,
            category_scores=category_scores,
            raw=body,
        )


def moderate_vendor_text(text: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    return OpenAIVendorTextSafetyClient(api_key=api_key).moderate(text).to_dict()
