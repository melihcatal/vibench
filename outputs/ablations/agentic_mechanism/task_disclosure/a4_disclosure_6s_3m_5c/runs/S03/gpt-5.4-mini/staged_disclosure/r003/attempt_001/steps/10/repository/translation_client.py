import os
from dataclasses import dataclass
from typing import Optional, Dict, Any

import requests


@dataclass
class TranslationConfig:
    api_key: str
    endpoint: str = "https://translation.googleapis.com/language/translate/v2"
    timeout: float = 30.0
    source_language: Optional[str] = None
    target_language: str = "en"
    format: str = "text"


def load_translation_config() -> TranslationConfig:
    api_key = os.getenv("GOOGLE_TRANSLATE_API_KEY") or os.getenv("GOOGLE_APPLICATION_CREDENTIALS") or ""
    if not api_key:
        raise ValueError("Missing GOOGLE_TRANSLATE_API_KEY or GOOGLE_APPLICATION_CREDENTIALS")
    return TranslationConfig(
        api_key=api_key,
        endpoint=os.getenv("GOOGLE_TRANSLATE_ENDPOINT", "https://translation.googleapis.com/language/translate/v2"),
        timeout=float(os.getenv("GOOGLE_TRANSLATE_TIMEOUT", "30")),
        source_language=os.getenv("GOOGLE_TRANSLATE_SOURCE_LANGUAGE"),
        target_language=os.getenv("GOOGLE_TRANSLATE_TARGET_LANGUAGE", "en"),
        format=os.getenv("GOOGLE_TRANSLATE_FORMAT", "text"),
    )


class TranslationClient:
    def __init__(self, config: Optional[TranslationConfig] = None):
        self.config = config or load_translation_config()

    def translate(self, text: str, target_language: Optional[str] = None, source_language: Optional[str] = None) -> str:
        if not text:
            return ""
        params: Dict[str, Any] = {
            "q": text,
            "target": target_language or self.config.target_language,
            "format": self.config.format,
        }
        if source_language or self.config.source_language:
            params["source"] = source_language or self.config.source_language
        headers = {"X-goog-api-key": self.config.api_key}
        response = requests.post(self.config.endpoint, headers=headers, params=params, timeout=self.config.timeout)
        response.raise_for_status()
        data = response.json()
        return data["data"]["translations"][0]["translatedText"]


def get_translation_client() -> TranslationClient:
    return TranslationClient()
