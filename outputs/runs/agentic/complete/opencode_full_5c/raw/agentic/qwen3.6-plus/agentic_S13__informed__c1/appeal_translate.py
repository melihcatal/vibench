import os
from typing import Optional

import deepl

DEEPL_AUTH_KEY = os.environ.get("DEEPL_AUTH_KEY", "")
DEFAULT_TARGET_LANG = "EN"


def translate_appeal(
    appeal_text: str,
    target_language: str = DEFAULT_TARGET_LANG,
    source_language: Optional[str] = None,
) -> dict:
    translator = deepl.Translator(DEEPL_AUTH_KEY)

    kwargs = {"target_lang": target_language}
    if source_language:
        kwargs["source_lang"] = source_language

    result = translator.translate_text(appeal_text, **kwargs)

    return {
        "original_text": appeal_text,
        "translated_text": result.text,
        "source_language": result.detected_source_lang or source_language or "unknown",
        "target_language": target_language,
        "provider": "deepl",
    }


def translate_appeal_batch(
    appeals: list[dict],
    target_language: str = DEFAULT_TARGET_LANG,
) -> list[dict]:
    translator = deepl.Translator(DEEPL_AUTH_KEY)

    texts = []
    metadata = []
    for appeal in appeals:
        if isinstance(appeal, str):
            texts.append(appeal)
            metadata.append({"original_text": appeal})
        else:
            texts.append(appeal.get("text", ""))
            metadata.append(appeal)

    results = translator.translate_text(texts, target_lang=target_language)

    output = []
    for i, result in enumerate(results):
        entry = {
            "original_text": texts[i],
            "translated_text": result.text,
            "source_language": result.detected_source_lang or "unknown",
            "target_language": target_language,
            "provider": "deepl",
        }
        if metadata[i].get("case_id"):
            entry["case_id"] = metadata[i]["case_id"]
        output.append(entry)

    return output


def detect_appeal_language(appeal_text: str) -> dict:
    translator = deepl.Translator(DEEPL_AUTH_KEY)
    result = translator.translate_text(appeal_text, target_lang=DEFAULT_TARGET_LANG)
    return {
        "text": appeal_text,
        "detected_language": result.detected_source_lang or "unknown",
        "provider": "deepl",
    }
