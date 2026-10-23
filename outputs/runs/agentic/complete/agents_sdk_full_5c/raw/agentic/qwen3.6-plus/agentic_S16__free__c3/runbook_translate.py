"""
Translate secret-rotation runbook notes using OpenAI translation.

This module uses the OpenAI chat completions API with gpt-4o-mini
at api.openai.com to translate runbook documentation for
secret rotation procedures.
"""

import logging
from typing import Optional

import openai
from openai import OpenAI

logger = logging.getLogger(__name__)

OPENAI_API_BASE = "https://api.openai.com/v1"
OPENAI_TRANSLATION_MODEL = "gpt-4o-mini"


def _get_openai_client() -> OpenAI:
    """Create an OpenAI client using the official SDK."""
    return OpenAI(
        api_key=__import__("os").environ.get("OPENAI_API_KEY", ""),
        base_url=OPENAI_API_BASE,
    )


def translate_runbook_notes(
    runbook_text: str,
    target_language: str = "en",
    source_language: Optional[str] = None,
) -> Optional[str]:
    """
    Translate secret-rotation runbook notes using OpenAI gpt-4o-mini.

    Args:
        runbook_text: The runbook notes text to translate.
        target_language: Target language code (e.g., 'en', 'es', 'fr').
        source_language: Source language code (auto-detected if None).

    Returns:
        Translated text or None on failure.
    """
    try:
        client = _get_openai_client()

        source_spec = f" from {source_language}" if source_language else ""
        system_prompt = (
            f"You are a technical documentation translator. "
            f"Translate the following secret-rotation runbook notes"
            f"{source_spec} into {target_language}. "
            f"Preserve technical terms, secret names, and code references exactly. "
            f"Only output the translated text."
        )

        response = client.chat.completions.create(
            model=OPENAI_TRANSLATION_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": runbook_text},
            ],
            temperature=0.1,
        )

        translated = response.choices[0].message.content
        logger.info(
            "Translated runbook notes using %s on api.openai.com",
            OPENAI_TRANSLATION_MODEL,
        )
        return translated

    except openai.APIError as e:
        logger.error("OpenAI translation API error: %s", str(e))
        return None
    except Exception as e:
        logger.error("Error translating runbook notes: %s", str(e))
        return None


def translate_runbook_batch(
    runbook_entries: list[dict],
    target_language: str = "en",
    notes_field: str = "runbook_notes",
    output_field: str = "translated_notes",
) -> list[dict]:
    """
    Translate multiple runbook entries in batch using OpenAI gpt-4o-mini.

    Args:
        runbook_entries: List of dicts containing runbook notes.
        target_language: Target language code.
        notes_field: Field containing original notes.
        output_field: Field to store translated notes.

    Returns:
        Updated list of entries with translated notes.
    """
    for entry in runbook_entries:
        original_notes = entry.get(notes_field, "")
        if original_notes:
            translated = translate_runbook_notes(
                original_notes,
                target_language=target_language,
            )
            entry[output_field] = translated
            entry["translation_model"] = OPENAI_TRANSLATION_MODEL
            entry["translation_provider"] = "openai"
        else:
            entry[output_field] = ""

    return runbook_entries
