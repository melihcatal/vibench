import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


DEFAULT_TRANSLATION_API_BASE_URL = "https://translation.googleapis.com/language/translate/v2"


@dataclass(frozen=True)
class TranslationConfig:
    api_key: str
    base_url: str = DEFAULT_TRANSLATION_API_BASE_URL
    timeout: float = 30.0


def load_translation_config() -> TranslationConfig:
    api_key = os.getenv("GOOGLE_TRANSLATE_API_KEY") or os.getenv("TRANSLATION_API_KEY")
    if not api_key:
        raise ValueError("Missing translation API key; set GOOGLE_TRANSLATE_API_KEY or TRANSLATION_API_KEY")
    base_url = os.getenv("TRANSLATION_API_BASE_URL", DEFAULT_TRANSLATION_API_BASE_URL)
    timeout_raw = os.getenv("TRANSLATION_API_TIMEOUT", "30")
    try:
        timeout = float(timeout_raw)
    except ValueError as exc:
        raise ValueError("TRANSLATION_API_TIMEOUT must be a number") from exc
    return TranslationConfig(api_key=api_key, base_url=base_url, timeout=timeout)


class TranslationClient:
    def __init__(self, config: Optional[TranslationConfig] = None) -> None:
        self.config = config or load_translation_config()
        self._session = requests.Session()

    def translate(self, text: str, target_language: str, source_language: Optional[str] = None, mime_type: str = "text/plain") -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "q": text,
            "target": target_language,
            "format": "text" if mime_type == "text/plain" else "html",
        }
        if source_language:
            payload["source"] = source_language
        params = {"key": self.config.api_key}
        response = self._session.post(self.config.base_url, params=params, json=payload, timeout=self.config.timeout)
        response.raise_for_status()
        data = response.json()
        translations = data.get("data", {}).get("translations", [])
        return translations[0] if translations else data

    def close(self) -> None:
        self._session.close()

    def __enter__(self) -> "TranslationClient":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()
