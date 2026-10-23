import os
import deepl
from typing import Optional
from security_models import TranslationResult


def translate_runbook_notes(
    text: str,
    target_language: str = "EN-US",
    source_language: Optional[str] = None,
    formality: str = "default",
) -> TranslationResult:
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    translator = deepl.Translator(auth_key)
    kwargs = {
        "target_lang": target_language,
        "formality": formality,
    }
    if source_language:
        kwargs["source_lang"] = source_language
    result = translator.translate_text(text, **kwargs)
    return TranslationResult(
        original_text=text,
        translated_text=result.text,
        source_language=result.detected_source_language,
        target_language=target_language,
        model="deepl",
    )


def translate_runbook_batch(
    texts: list[str],
    target_language: str = "EN-US",
    source_language: Optional[str] = None,
    formality: str = "default",
) -> list[TranslationResult]:
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    translator = deepl.Translator(auth_key)
    kwargs = {
        "target_lang": target_language,
        "formality": formality,
    }
    if source_language:
        kwargs["source_lang"] = source_language
    results = translator.translate_text(texts, **kwargs)
    output = []
    for i, result in enumerate(results):
        output.append(
            TranslationResult(
                original_text=texts[i],
                translated_text=result.text,
                source_language=result.detected_source_language,
                target_language=target_language,
                model="deepl",
            )
        )
    return output


def translate_rotation_runbook(
    runbook_text: str,
    target_languages: list[str],
    source_language: Optional[str] = None,
) -> list[TranslationResult]:
    translations = []
    for lang in target_languages:
        result = translate_runbook_notes(
            text=runbook_text,
            target_language=lang,
            source_language=source_language,
        )
        translations.append(result)
    return translations
