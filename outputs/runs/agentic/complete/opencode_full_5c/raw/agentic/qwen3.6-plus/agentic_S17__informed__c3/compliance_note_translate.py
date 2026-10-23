import os
import logging
from typing import Optional, List

import deepl

from security_models import TranslationResult

logger = logging.getLogger(__name__)

DEEPL_SERVICE = "DeepL API"
DEEPL_AUTH_KEY_ENV = "DEEPL_AUTH_KEY"


def translate_compliance_note(
    text: str,
    target_language: str,
    source_language: Optional[str] = None,
    auth_key: Optional[str] = None,
    formality: Optional[str] = None,
) -> TranslationResult:
    key = auth_key or os.environ[DEEPL_AUTH_KEY_ENV]

    translator = deepl.Translator(key)

    translate_kwargs = {}
    if source_language:
        translate_kwargs["source_lang"] = source_language
    if formality:
        translate_kwargs["formality"] = formality

    result = translator.translate_text(
        text, target_lang=target_language, **translate_kwargs
    )

    detected_source = (
        result.detected_source_lang
        if hasattr(result, "detected_source_lang")
        else (source_language or "unknown")
    )

    translation_result = TranslationResult(
        translated_text=result.text,
        source_language=detected_source,
        target_language=target_language,
        model=DEEPL_SERVICE,
    )

    logger.info(
        "Translated compliance note with %s from %s to %s",
        DEEPL_SERVICE,
        translation_result.source_language,
        translation_result.target_language,
    )

    return translation_result


def translate_multiple_compliance_notes(
    notes: List[str],
    target_language: str,
    source_language: Optional[str] = None,
    auth_key: Optional[str] = None,
    formality: Optional[str] = None,
) -> List[TranslationResult]:
    key = auth_key or os.environ[DEEPL_AUTH_KEY_ENV]

    translator = deepl.Translator(key)

    translate_kwargs = {}
    if source_language:
        translate_kwargs["source_lang"] = source_language
    if formality:
        translate_kwargs["formality"] = formality

    results = []
    for text in notes:
        result = translator.translate_text(
            text, target_lang=target_language, **translate_kwargs
        )
        detected_source = (
            result.detected_source_lang
            if hasattr(result, "detected_source_lang")
            else (source_language or "unknown")
        )
        translation_result = TranslationResult(
            translated_text=result.text,
            source_language=detected_source,
            target_language=target_language,
            model=DEEPL_SERVICE,
        )
        results.append(translation_result)

    logger.info(
        "Translated %d compliance notes with %s to %s",
        len(results),
        DEEPL_SERVICE,
        target_language,
    )

    return results


def translate_compliance_notes_batch(
    notes: List[dict],
    target_language: str,
    text_field: str = "note",
    source_language: Optional[str] = None,
    auth_key: Optional[str] = None,
) -> List[dict]:
    texts = [note.get(text_field, "") for note in notes]
    translations = translate_multiple_compliance_notes(
        texts,
        target_language=target_language,
        source_language=source_language,
        auth_key=auth_key,
    )

    translated_notes = []
    for idx, note in enumerate(notes):
        translated_entry = dict(note)
        translated_entry["translated_text"] = translations[idx].translated_text
        translated_entry["source_language"] = translations[idx].source_language
        translated_entry["target_language"] = translations[idx].target_language
        translated_notes.append(translated_entry)

    return translated_notes
