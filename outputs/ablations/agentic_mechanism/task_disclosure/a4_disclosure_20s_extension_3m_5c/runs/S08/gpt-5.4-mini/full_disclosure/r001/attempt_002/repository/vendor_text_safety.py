from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional

import requests


@dataclass
class VendorTextSafetyConfig:
    api_key: str
    model: str = "omni-moderation-latest"
    base_url: str = "https://api.openai.com/v1"
    timeout: float = 30.0


def load_vendor_text_safety_config(env: Optional[Mapping[str, str]] = None) -> VendorTextSafetyConfig:
    source = env if env is not None else os.environ
    api_key = source.get("OPENAI_API_KEY", "")
    model = source.get("OPENAI_MODERATION_MODEL", "omni-moderation-latest")
    base_url = source.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
    timeout_raw = source.get("OPENAI_TIMEOUT", "30")
    try:
        timeout = float(timeout_raw)
    except (TypeError, ValueError):
        timeout = 30.0
    return VendorTextSafetyConfig(api_key=api_key, model=model, base_url=base_url.rstrip("/"), timeout=timeout)


class VendorTextSafetyClient:
    def __init__(self, config: Optional[VendorTextSafetyConfig] = None):
        self.config = config or load_vendor_text_safety_config()

    def _headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.config.api_key:
            headers["Authorization"] = f"Bearer {self.config.api_key}"
        return headers

    def moderate(self, text: str) -> Dict[str, Any]:
        payload = {"model": self.config.model, "input": text}
        response = requests.post(f"{self.config.base_url}/moderations", headers=self._headers(), json=payload, timeout=self.config.timeout)
        response.raise_for_status()
        return response.json()


def moderate_vendor_text(text: Optional[str], env: Optional[Mapping[str, str]] = None) -> Dict[str, Any]:
    client = VendorTextSafetyClient(load_vendor_text_safety_config(env))
    content = text or ""
    response = client.moderate(content)
    result = response.get("results") or []
    item = result[0] if result else {}
    categories = item.get("categories") or {}
    category_scores = item.get("category_scores") or {}
    flagged = bool(item.get("flagged", False))
    return {
        "input": content,
        "flagged": flagged,
        "categories": categories,
        "category_scores": category_scores,
        "model": response.get("model", client.config.model),
        "raw": response,
    }
