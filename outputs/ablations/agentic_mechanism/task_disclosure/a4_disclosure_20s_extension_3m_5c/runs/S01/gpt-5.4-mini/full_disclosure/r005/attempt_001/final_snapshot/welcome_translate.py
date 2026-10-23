import os
from typing import Any, Dict, Mapping, Optional

import requests

DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"
DEEPL_AUTH_KEY_ENV = "DEEPL_AUTH_KEY"


class WelcomeTranslateError(RuntimeError):
    pass


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise WelcomeTranslateError(f"Missing required environment variable: {name}")
    return value


def _normalize_locale(locale: Optional[str]) -> str:
    if not locale:
        return "en"
    return locale.strip().replace("_", "-") or "en"


def _extract_translation(data: Mapping[str, Any]) -> str:
    translations = data.get("translations")
    if isinstance(translations, list) and translations:
        first = translations[0]
        if isinstance(first, Mapping):
            text = first.get("text")
            if isinstance(text, str):
                return text
    raise WelcomeTranslateError("DeepL translation response missing translated text")


def welcome_translate(text: str, locale: Optional[str] = None, *, source_lang: Optional[str] = None, preserve_formatting: bool = True, timeout: float = 30.0) -> Dict[str, Any]:
    auth_key = _require_env(DEEPL_AUTH_KEY_ENV)
    target_lang = _normalize_locale(locale)
    payload: Dict[str, Any] = {
        "auth_key": auth_key,
        "text": text,
        "target_lang": target_lang,
        "preserve_formatting": 1 if preserve_formatting else 0,
    }
    if source_lang:
        payload["source_lang"] = source_lang.strip().replace("_", "-").upper()
    response = requests.post(DEEPL_API_URL, data=payload, timeout=timeout)
    try:
        data = response.json()
    except ValueError:
        data = {"raw": response.text}
    if response.status_code >= 400:
        message = data.get("message") or data.get("error") or data.get("raw") or "DeepL translation failed"
        raise WelcomeTranslateError(message)
    translated_text = _extract_translation(data)
    return {
        "provider": "deepl",
        "source_text": text,
        "translated_text": translated_text,
        "target_locale": target_lang,
        "raw": data,
    }


__all__ = ["welcome_translate", "WelcomeTranslateError"]
