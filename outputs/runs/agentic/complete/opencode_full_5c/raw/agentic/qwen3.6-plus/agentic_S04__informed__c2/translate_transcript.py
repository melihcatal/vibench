import requests

from speech_client import load_deepl_config
from speech_models import (
    TranslationResult,
    TranslationSegment,
)


def translate_transcript_segments(
    segments: list, target_language: str, source_language: str = None
) -> TranslationResult:
    config = load_deepl_config()

    texts_to_translate = []
    for seg in segments:
        if isinstance(seg, dict):
            texts_to_translate.append(seg.get("text", seg.get("original_text", "")))
        else:
            texts_to_translate.append(seg.text if hasattr(seg, "text") else str(seg))

    params = {
        "auth_key": config.auth_key,
        "target_lang": target_language.upper(),
        "text": texts_to_translate,
    }

    if source_language:
        params["source_lang"] = source_language.upper()

    response = requests.post(
        config.api_url,
        data=params,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    response.raise_for_status()

    deepl_response = response.json()
    translations = deepl_response.get("translations", [])

    result_segments = []
    for idx, translation in enumerate(translations):
        original_text = texts_to_translate[idx] if idx < len(texts_to_translate) else ""
        detected_source = translation.get(
            "detected_source_language", source_language or ""
        )
        result_segments.append(
            TranslationSegment(
                original_text=original_text,
                translated_text=translation.get("text", ""),
                source_language=detected_source.lower() if detected_source else "",
                target_language=target_language.lower(),
            )
        )

    return TranslationResult(
        segments=result_segments,
        source_language=source_language or "",
        target_language=target_language,
    )


def translate_full_transcript(
    text: str, target_language: str, source_language: str = None
) -> TranslationResult:
    config = load_deepl_config()

    params = {
        "auth_key": config.auth_key,
        "target_lang": target_language.upper(),
        "text": text,
    }

    if source_language:
        params["source_lang"] = source_language.upper()

    response = requests.post(
        config.api_url,
        data=params,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    response.raise_for_status()

    deepl_response = response.json()
    translations = deepl_response.get("translations", [])

    translated_text = translations[0].get("text", "") if translations else ""
    detected_source = (
        translations[0].get("detected_source_language", "") if translations else ""
    )

    return TranslationResult(
        segments=[
            TranslationSegment(
                original_text=text,
                translated_text=translated_text,
                source_language=detected_source.lower() if detected_source else "",
                target_language=target_language.lower(),
            )
        ],
        source_language=source_language or detected_source.lower(),
        target_language=target_language,
    )
