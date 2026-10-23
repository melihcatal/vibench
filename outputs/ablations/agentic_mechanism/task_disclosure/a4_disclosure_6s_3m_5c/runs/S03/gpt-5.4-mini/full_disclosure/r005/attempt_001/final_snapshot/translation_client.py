import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")


@dataclass(frozen=True)
class TranslationClientConfig:
    api_key: str
    base_url: str = OPENAI_API_BASE
    model: str = OPENAI_MODEL
    timeout: float = 60.0


def load_translation_client_config(
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    model: Optional[str] = None,
    timeout: Optional[float] = None,
) -> TranslationClientConfig:
    key = api_key or os.getenv(OPENAI_API_KEY_ENV, "")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")
    return TranslationClientConfig(
        api_key=key,
        base_url=base_url or OPENAI_API_BASE,
        model=model or OPENAI_MODEL,
        timeout=timeout if timeout is not None else 60.0,
    )


class TranslationClient:
    def __init__(self, config: TranslationClientConfig):
        self.config = config
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Authorization": f"Bearer {config.api_key}",
                "Content-Type": "application/json",
            }
        )

    @property
    def chat_completions_url(self) -> str:
        return self.config.base_url.rstrip("/") + "/chat/completions"

    def post(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = self._session.post(
            self.chat_completions_url,
            json=payload,
            timeout=self.config.timeout,
        )
        response.raise_for_status()
        return response.json()

    def translate(self, text: str, source_language: str, target_language: str) -> str:
        payload = {
            "model": self.config.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a translation engine that preserves meaning, formatting, and intent.",
                },
                {
                    "role": "user",
                    "content": {
                        "text": text,
                        "source_language": source_language,
                        "target_language": target_language,
                    },
                },
            ],
            "temperature": 0,
        }
        data = self.post(payload)
        return data["choices"][0]["message"]["content"]


def create_translation_client(
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    model: Optional[str] = None,
    timeout: Optional[float] = None,
) -> TranslationClient:
    return TranslationClient(
        load_translation_client_config(api_key=api_key, base_url=base_url, model=model, timeout=timeout)
    )
