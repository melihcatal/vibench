import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


@dataclass(frozen=True)
class TranslationClientConfig:
    api_key: str
    base_url: str = "https://api.openai.com/v1"
    model: str = "gpt-4.1-mini"
    timeout: float = 30.0


def load_translation_client_config(env: Optional[Dict[str, str]] = None) -> TranslationClientConfig:
    source = env if env is not None else os.environ
    api_key = source.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    base_url = source.get("TRANSLATION_API_BASE_URL", "https://api.openai.com/v1").strip() or "https://api.openai.com/v1"
    model = source.get("TRANSLATION_MODEL", "gpt-4.1-mini").strip() or "gpt-4.1-mini"
    timeout_raw = source.get("TRANSLATION_TIMEOUT_SECONDS", "30").strip()
    try:
        timeout = float(timeout_raw)
    except ValueError as exc:
        raise ValueError("TRANSLATION_TIMEOUT_SECONDS must be a number") from exc
    return TranslationClientConfig(api_key=api_key, base_url=base_url, model=model, timeout=timeout)


class TranslationClient:
    def __init__(self, config: Optional[TranslationClientConfig] = None, env: Optional[Dict[str, str]] = None):
        self.config = config or load_translation_client_config(env)

    def headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
        }

    def chat_completions_url(self) -> str:
        return f"{self.config.base_url.rstrip('/')}/chat/completions"

    def request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = requests.post(
            self.chat_completions_url(),
            headers=self.headers(),
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
                    "content": "You are a translation engine. Return only the translated text.",
                },
                {
                    "role": "user",
                    "content": f"Translate from {source_language} to {target_language}: {text}",
                },
            ],
            "temperature": 0,
        }
        data = self.request(payload)
        return data["choices"][0]["message"]["content"].strip()
