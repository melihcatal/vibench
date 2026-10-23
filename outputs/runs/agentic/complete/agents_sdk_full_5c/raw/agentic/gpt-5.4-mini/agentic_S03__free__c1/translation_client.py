import os
from dataclasses import dataclass
from typing import Optional

import requests

DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"
DEEPL_AUTH_KEY_ENV = "DEEPL_AUTH_KEY"


@dataclass
class TranslationClientConfig:
    auth_key: str
    api_url: str = DEEPL_API_URL
    timeout: float = 30.0


def load_config(auth_key: Optional[str] = None) -> TranslationClientConfig:
    key = auth_key or os.getenv(DEEPL_AUTH_KEY_ENV, "")
    if not key:
        raise ValueError(f"Missing {DEEPL_AUTH_KEY_ENV}")
    return TranslationClientConfig(auth_key=key)


def client_headers(cfg: TranslationClientConfig) -> dict:
    return {"Authorization": f"DeepL-Auth-Key {cfg.auth_key}"}


def post_translate(data: dict, cfg: Optional[TranslationClientConfig] = None) -> dict:
    cfg = cfg or load_config()
    resp = requests.post(cfg.api_url, data=data, headers=client_headers(cfg), timeout=cfg.timeout)
    resp.raise_for_status()
    return resp.json()
