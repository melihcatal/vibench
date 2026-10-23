from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests


DEEPL_API_URL = os.getenv("DEEPL_API_URL", "https://api.deepl.com/v2/translate")
DEEPL_AUTH_KEY_ENV = "DEEPL_AUTH_KEY"


class DeepLTranslationClient:
    def __init__(self, auth_key: Optional[str] = None, timeout: float = 30.0) -> None:
        self.auth_key = auth_key or os.getenv(DEEPL_AUTH_KEY_ENV)
        if not self.auth_key:
            raise ValueError(f"Missing {DEEPL_AUTH_KEY_ENV}")
        self.timeout = timeout

    def translate(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = requests.post(
            DEEPL_API_URL,
            headers={
                "Authorization": f"DeepL-Auth-Key {self.auth_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()
