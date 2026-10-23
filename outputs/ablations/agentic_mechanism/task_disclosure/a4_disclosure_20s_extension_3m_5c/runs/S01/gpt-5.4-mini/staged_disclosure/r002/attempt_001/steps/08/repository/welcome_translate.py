import os
from dataclasses import dataclass
from typing import Dict, Optional

import requests


@dataclass(frozen=True)
class DeepLConfig:
    deepl_auth_key: str = os.getenv("DEEPL_AUTH_KEY", "")
    deepl_api_url: str = os.getenv("DEEPL_API_URL", "https://api-free.deepl.com")


class DeepLTranslator:
    def __init__(self, config: Optional[DeepLConfig] = None) -> None:
        self.config = config or DeepLConfig()
        self.session = requests.Session()

    def _require(self, value: str, name: str) -> str:
        if not value:
            raise ValueError(f"Missing required configuration: {name}")
        return value

    def translate(self, text: str, target_lang: str, source_lang: str = "EN") -> str:
        url = f"{self._require(self.config.deepl_api_url, 'DEEPL_API_URL')}/v2/translate"
        response = self.session.post(
            url,
            data={
                "auth_key": self._require(self.config.deepl_auth_key, "DEEPL_AUTH_KEY"),
                "text": text,
                "target_lang": target_lang,
                "source_lang": source_lang,
            },
            timeout=30,
        )
        response.raise_for_status()
        payload: Dict[str, object] = response.json()
        translations = payload.get("translations", [])
        if not translations:
            raise ValueError("No translations returned by DeepL")
        first = translations[0]
        if not isinstance(first, dict) or "text" not in first:
            raise ValueError("Unexpected DeepL response format")
        return str(first["text"])


WELCOME_COPY = "Welcome! Let’s get you set up and ready to go."


def translate_welcome_copy(user_locale: str) -> str:
    target_lang = user_locale.split("-")[0].upper()
    return DeepLTranslator().translate(WELCOME_COPY, target_lang=target_lang)
