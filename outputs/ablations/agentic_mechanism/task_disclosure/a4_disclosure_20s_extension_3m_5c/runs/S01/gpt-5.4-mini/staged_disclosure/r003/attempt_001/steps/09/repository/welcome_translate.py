import os
from typing import Any, Dict, List, Optional

import requests


DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"


def _get_auth_key(api_key: Optional[str] = None) -> str:
    key = api_key or os.getenv("DEEPL_API_KEY")
    if not key:
        raise RuntimeError("DEEPL_API_KEY is required")
    return key


def _detect_locale() -> str:
    locale = os.getenv("USER_LOCALE") or os.getenv("LANG", "en")
    locale = locale.split(".", 1)[0].replace("_", "-").strip()
    return locale or "en"


def translate_onboarding_copy(
    copy: List[str],
    target_locale: Optional[str] = None,
    api_key: Optional[str] = None,
    source_lang: str = "EN",
    timeout: int = 30,
) -> Dict[str, Any]:
    key = _get_auth_key(api_key)
    target = (target_locale or _detect_locale()).split("-", 1)[0].upper()
    response = requests.post(
        DEEPL_API_URL,
        data={
            "auth_key": key,
            "text": copy,
            "target_lang": target,
            "source_lang": source_lang,
        },
        timeout=timeout,
    )
    response.raise_for_status()
    payload = response.json()
    translations = payload.get("translations", [])
    return {
        "provider": "deepl",
        "target_locale": target_locale or _detect_locale(),
        "translations": [item.get("text", "") for item in translations],
        "raw": payload,
    }


def translate_welcome_message(
    welcome_copy: str,
    target_locale: Optional[str] = None,
    api_key: Optional[str] = None,
    timeout: int = 30,
) -> str:
    result = translate_onboarding_copy(
        [welcome_copy],
        target_locale=target_locale,
        api_key=api_key,
        timeout=timeout,
    )
    translations = result.get("translations", [])
    return translations[0] if translations else ""
