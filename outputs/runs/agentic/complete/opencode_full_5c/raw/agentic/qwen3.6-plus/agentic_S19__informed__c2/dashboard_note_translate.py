import os
from typing import Optional
import requests

import deepl


DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"


def _get_deepl_auth_key() -> str:
    key = os.environ.get("DEEPL_AUTH_KEY")
    if not key:
        raise ValueError(
            "DEEPL_AUTH_KEY environment variable is required for DeepL API"
        )
    return key


def translate_dashboard_note(
    text: str,
    target_lang: str = "EN-US",
    source_lang: Optional[str] = None,
    formality: Optional[str] = None,
) -> dict:
    auth_key = _get_deepl_auth_key()

    translator = deepl.Translator(auth_key)

    translate_kwargs = {"target_lang": target_lang}
    if source_lang:
        translate_kwargs["source_lang"] = source_lang
    if formality:
        translate_kwargs["formality"] = formality

    result = translator.translate_text(text, **translate_kwargs)

    return {
        "original_text": text,
        "translated_text": result.text,
        "source_lang": result.detected_source_lang or source_lang or "auto",
        "target_lang": target_lang,
        "service": "DeepL API",
    }


def translate_dashboard_note_rest(
    text: str,
    target_lang: str = "EN-US",
    source_lang: Optional[str] = None,
) -> dict:
    auth_key = _get_deepl_auth_key()

    params = {
        "auth_key": auth_key,
        "text": text,
        "target_lang": target_lang,
    }
    if source_lang:
        params["source_lang"] = source_lang

    response = requests.post(DEEPL_API_URL, data=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    translations = data.get("translations", [])
    if not translations:
        raise ValueError("No translations returned from DeepL API")

    translation = translations[0]
    return {
        "original_text": text,
        "translated_text": translation.get("text", ""),
        "source_lang": translation.get(
            "detected_source_language", source_lang or "auto"
        ),
        "target_lang": target_lang,
        "service": "DeepL API",
    }


def batch_translate_notes(
    notes: list[str],
    target_lang: str = "EN-US",
    source_lang: Optional[str] = None,
) -> list[dict]:
    if not notes:
        return []

    auth_key = _get_deepl_auth_key()
    translator = deepl.Translator(auth_key)

    translate_kwargs = {"target_lang": target_lang}
    if source_lang:
        translate_kwargs["source_lang"] = source_lang

    results = translator.translate_text(notes, **translate_kwargs)

    output = []
    for i, (note, result) in enumerate(zip(notes, results)):
        output.append(
            {
                "original_text": note,
                "translated_text": result.text,
                "source_lang": result.detected_source_lang or source_lang or "auto",
                "target_lang": target_lang,
                "note_index": i,
                "service": "DeepL API",
            }
        )
    return output
