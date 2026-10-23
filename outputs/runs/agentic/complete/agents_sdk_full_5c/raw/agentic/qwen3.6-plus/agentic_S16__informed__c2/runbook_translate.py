"""Translate secret-rotation runbook notes using DeepL API.

Provider: DeepL API (deepl SDK)
Auth: DEEPL_AUTH_KEY
"""

import os
from typing import List

import deepl


def translate_runbook_notes(
    notes: str,
    target_lang: str = "EN-US",
    source_lang: str | None = None,
) -> dict:
    """Translate secret-rotation runbook notes using the DeepL translation API.

    Returns the translated text and metadata.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        return {
            "status": "error",
            "error": "DEEPL_AUTH_KEY environment variable not set",
            "provider": "deepl",
        }

    if not notes or not notes.strip():
        return {
            "status": "no_content",
            "translated_text": "",
            "provider": "deepl",
        }

    try:
        translator = deepl.Translator(auth_key)

        translate_options: dict = {
            "target_lang": target_lang,
        }
        if source_lang:
            translate_options["source_lang"] = source_lang

        result = translator.translate_text(notes, **translate_options)

        return {
            "status": "success",
            "original_text": notes,
            "translated_text": result.text,
            "source_lang": result.detected_source_lang if hasattr(result, "detected_source_lang") else source_lang or "auto",
            "target_lang": target_lang,
            "provider": "deepl",
        }

    except deepl.DeepLException as exc:
        return {
            "status": "error",
            "error": str(exc),
            "provider": "deepl",
        }


def translate_batch_runbook_notes(
    notes_list: List[str],
    target_lang: str = "EN-US",
) -> dict:
    """Translate multiple runbook note entries using DeepL batch translation."""
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        return {
            "status": "error",
            "error": "DEEPL_AUTH_KEY environment variable not set",
            "provider": "deepl",
        }

    try:
        translator = deepl.Translator(auth_key)

        results = translator.translate_text(
            notes_list,
            target_lang=target_lang,
        )

        translations = [
            {
                "original": original,
                "translated": translated.text,
            }
            for original, translated in zip(notes_list, results)
        ]

        return {
            "status": "success",
            "translations": translations,
            "count": len(translations),
            "target_lang": target_lang,
            "provider": "deepl",
        }

    except deepl.DeepLException as exc:
        return {
            "status": "error",
            "error": str(exc),
            "provider": "deepl",
        }


def translate_rotation_runbook(
    rotation_summary: dict,
    target_lang: str = "EN-US",
) -> dict:
    """Translate key fields from a rotation summary into the target language."""
    sections = []
    if rotation_summary.get("secret_name"):
        sections.append(f"Secret: {rotation_summary['secret_name']}")
    if rotation_summary.get("rotation_enabled"):
        sections.append(f"Rotation enabled: {rotation_summary['rotation_enabled']}")
    if rotation_summary.get("last_rotation_date"):
        sections.append(f"Last rotated: {rotation_summary['last_rotation_date']}")
    if rotation_summary.get("error"):
        sections.append(f"Error: {rotation_summary['error']}")

    combined = " | ".join(sections) if sections else "No summary data available."
    return translate_runbook_notes(combined, target_lang=target_lang)


if __name__ == "__main__":
    result = translate_runbook_notes(
        notes="Rotación programada de credenciales de base de datos completada exitosamente.",
        source_lang="ES",
        target_lang="EN-US",
    )
    print(f"Status: {result.get('status')}")
    print(f"Translation: {result.get('translated_text')}")
