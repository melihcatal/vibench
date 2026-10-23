import os
import deepl
from safety_models import AppealTranslation

DEEPL_API_KEY = os.environ.get("DEEPL_API_KEY", "")
DEEPL_API_URL = "https://api.deepl.com"
DEEPL_TARGET_LANGUAGE = os.environ.get("DEEPL_TARGET_LANGUAGE", "EN")


def translate_appeal(appeal_text, target_language=None, source_language=None):
    auth_key = DEEPL_API_KEY
    translator = deepl.Translator(auth_key, server_url=DEEPL_API_URL)
    target = target_language or DEEPL_TARGET_LANGUAGE

    translate_options = {}
    if source_language:
        translate_options["source_lang"] = source_language

    result = translator.translate_text(
        appeal_text, target_lang=target, **translate_options
    )
    detected_source = (
        result.detected_source_lang
        if hasattr(result, "detected_source_lang")
        else "UNKNOWN"
    )

    return AppealTranslation(
        original_text=appeal_text,
        translated_text=result.text,
        source_language=detected_source,
        target_language=target,
    )


def translate_appeal_batch(appeal_texts, target_language=None, source_language=None):
    auth_key = DEEPL_API_KEY
    translator = deepl.Translator(auth_key, server_url=DEEPL_API_URL)
    target = target_language or DEEPL_TARGET_LANGUAGE

    translate_options = {}
    if source_language:
        translate_options["source_lang"] = source_language

    results = translator.translate_text(
        appeal_texts, target_lang=target, **translate_options
    )
    translations = []
    for original, result in zip(appeal_texts, results):
        detected_source = (
            result.detected_source_lang
            if hasattr(result, "detected_source_lang")
            else "UNKNOWN"
        )
        translations.append(
            AppealTranslation(
                original_text=original,
                translated_text=result.text,
                source_language=detected_source,
                target_language=target,
            )
        )
    return translations
