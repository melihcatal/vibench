"""Translate secret-rotation runbook notes using DeepL API."""

import os
from typing import Any
import deepl


def translate_runbook_notes(
    text: str,
    target_lang: str = "EN-US",
    source_lang: str | None = None,
    formality: str = "default",
) -> dict[str, Any]:
    """Translate secret-rotation runbook notes via DeepL.

    Args:
        text: The runbook note text to translate.
        target_lang: Target language code (e.g., 'EN-US', 'DE', 'JA', 'FR').
            Defaults to 'EN-US'.
        source_lang: Source language code. If None, DeepL auto-detects.
        formality: Formality level. Options: 'default', 'more', 'less', 'prefer_less',
            'prefer_more'. Defaults to 'default'.

    Returns:
        A dict with 'translated_text', 'source_lang', 'target_lang'.

    Raises:
        ValueError: If DEEPL_AUTH_KEY is not set.
        deepl.DeepLException: If the DeepL API call fails.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")

    translator = deepl.Translator(auth_key)

    translate_kwargs: dict[str, Any] = {
        "target_lang": target_lang,
        "formality": formality,
    }
    if source_lang:
        translate_kwargs["source_lang"] = source_lang

    result = translator.translate_text(text, **translate_kwargs)

    return {
        "translated_text": result.text,
        "source_lang": result.detected_source_lang,
        "target_lang": target_lang,
    }


def translate_runbook_batch(
    notes: list[dict[str, str]],
    target_lang: str = "EN-US",
    text_field: str = "note",
) -> list[dict[str, Any]]:
    """Translate a batch of runbook notes.

    Args:
        notes: A list of dicts, each containing a note under `text_field`.
        target_lang: Target language code.
        text_field: The key containing the text to translate.

    Returns:
        A list of dicts with original metadata plus translated text.
    """
    texts = [note.get(text_field, "") for note in notes]
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")

    translator = deepl.Translator(auth_key)
    results = translator.translate_text(texts, target_lang=target_lang)

    output = []
    for i, note in enumerate(notes):
        translated = results[i].text if i < len(results) else ""
        output.append({
            **note,
            "translated_text": translated,
            "source_lang": results[i].detected_source_lang if i < len(results) else None,
        })
    return output


if __name__ == "__main__":
    sample = "Se ha rotado la clave de API debido a una posible filtración."
    result = translate_runbook_notes(sample, target_lang="EN-US")
    print(f"Source: {result['source_lang']}")
    print(f"Translation: {result['translated_text']}")
