from __future__ import annotations

from typing import Any, Dict

import requests

from identity_client import get_identity_config, make_headers

COHERE_TRANSLATE_MODEL = "command-r-plus-08-2024"


def welcome_translate(text: str, locale: str) -> str:
    cfg = get_identity_config()
    resp = requests.post(
        "https://api.cohere.com/v1/chat",
        headers={
            **make_headers(cfg),
            "Authorization": f"Bearer {cfg.client_secret}",
        },
        json={
            "model": COHERE_TRANSLATE_MODEL,
            "message": f"Translate the following onboarding copy into {locale}. Return only the translated text.\n\n{text}",
            "temperature": 0.2,
        },
        timeout=cfg.timeout_seconds,
    )
    resp.raise_for_status()
    data: Dict[str, Any] = resp.json() if resp.content else {}
    return data.get("text") or data.get("message") or text
