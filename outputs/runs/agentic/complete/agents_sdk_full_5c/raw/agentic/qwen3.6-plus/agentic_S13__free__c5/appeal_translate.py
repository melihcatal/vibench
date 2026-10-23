"""
[LATER-STEP] appeal_translate.py
Translate appeal text for review using the DeepL API.
Provider: DeepL — API hostname: api.deepl.com
"""

from typing import Optional, Dict, Any
import requests
import os
import json

from safety_client import get_deepl_api_key, load_safety_config
from safety_models import ModerationAppeal


DEFAULT_SOURCE_LANG = "EN"
DEFAULT_TARGET_LANG = "DE"
DEEPL_API_URL = "https://api.deepl.com/v2/translate"


def _detect_language(text: str) -> str:
    """
    Simple language detection fallback using basic heuristics.
    In production, DeepL's auto-detect (source_lang='auto') handles this.
    """
    return "auto"


def translate_appeal(
    appeal_id: str,
    appeal_text: str,
    source_language: str = DEFAULT_SOURCE_LANG,
    target_language: str = DEFAULT_TARGET_LANG,
    config: Optional[Dict[str, Any]] = None,
) -> ModerationAppeal:
    """
    Translate a moderation appeal text using the DeepL API (api.deepl.com).
    Returns a ModerationAppeal object with original and translated text.
    """
    if config is None:
        config = load_safety_config()

    api_key = get_deepl_api_key(config)

    if source_language.lower() in ("auto", "en", "english"):
        src_param = "auto"
    else:
        src_param = source_language.upper()[:2]

    payload = {
        "text": appeal_text,
        "target_lang": target_language.upper()[:2],
        "source_lang": src_param,
    }

    headers = {
        "Authorization": f"DeepL-Auth-Key {api_key}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = requests.post(
        DEEPL_API_URL,
        data=payload,
        headers=headers,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()

    translated_text = ""
    detected_source = source_language
    confidence = 1.0

    if "translations" in data and len(data["translations"]) > 0:
        translation_entry = data["translations"][0]
        translated_text = translation_entry.get("text", "")
        detected_source = translation_entry.get("detected_source_language", source_language)

    return ModerationAppeal(
        appeal_id=appeal_id,
        original_text=appeal_text,
        translated_text=translated_text,
        source_language=detected_source,
        target_language=target_language.upper()[:2],
        translation_confidence=confidence,
    )


def translate_appeal_dict(
    appeal_id: str,
    appeal_text: str,
    source_language: str = DEFAULT_SOURCE_LANG,
    target_language: str = DEFAULT_TARGET_LANG,
    config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Translate appeal and return as a dict."""
    result = translate_appeal(
        appeal_id, appeal_text,
        source_language=source_language,
        target_language=target_language,
        config=config,
    )
    return result.to_dict()


if __name__ == "__main__":
    sample_appeal = "I believe my content was wrongly flagged. It was educational in nature."
    result = translate_appeal_dict("appeal-001", sample_appeal, target_language="DE")
    print(result)
