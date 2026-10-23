import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


@dataclass(frozen=True)
class SafetyConfig:
    api_key: str
    base_url: str = "https://api.openai.com/v1"
    model: str = "text-moderation-latest"

    @classmethod
    def from_env(cls) -> "SafetyConfig":
        api_key = os.getenv("OPENAI_API_KEY", "").strip()
        if not api_key:
            raise ValueError("OPENAI_API_KEY is required")
        base_url = os.getenv("OPENAI_API_BASE", cls.base_url).rstrip("/")
        model = os.getenv("OPENAI_MODERATION_MODEL", cls.model).strip() or cls.model
        return cls(api_key=api_key, base_url=base_url, model=model)


class TextContentSafetyClient:
    def __init__(self, config: Optional[SafetyConfig] = None) -> None:
        self.config = config or SafetyConfig.from_env()
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Authorization": f"Bearer {self.config.api_key}",
                "Content-Type": "application/json",
            }
        )

    def moderate(self, text: str) -> Dict[str, Any]:
        if not isinstance(text, str):
            raise TypeError("text must be a string")
        response = self._session.post(
            f"{self.config.base_url}/moderations",
            json={"model": self.config.model, "input": text},
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    def is_safe(self, text: str) -> bool:
        result = self.moderate(text)
        outputs = result.get("results", [])
        if not outputs:
            return True
        return not bool(outputs[0].get("flagged", False))

    def close(self) -> None:
        self._session.close()


def load_safety_client() -> TextContentSafetyClient:
    return TextContentSafetyClient()
