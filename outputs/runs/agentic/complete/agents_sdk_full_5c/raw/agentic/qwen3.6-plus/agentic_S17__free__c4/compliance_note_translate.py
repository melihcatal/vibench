"""
Translate encryption or compliance notes for reviewers using the OpenAI Chat Completions API.
Uses the openai python SDK to translate technical encryption and compliance notes
between languages for international audit reviewers.

Provider: OpenAI Chat Completions API - api.openai.com
Model: gpt-4o-mini
"""

import json
import logging
import os
from typing import Optional, List, Dict, Any

from openai import OpenAI

from security_models import TranslationRequest, TranslationResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# OpenAI Chat model for translation
OPENAI_TRANSLATION_MODEL = "gpt-4o-mini"

# Supported languages for compliance note translation
SUPPORTED_LANGUAGES = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "ja": "Japanese",
    "zh": "Chinese",
    "pt": "Portuguese",
    "ko": "Korean",
    "it": "Italian",
    "ru": "Russian",
}


def create_openai_client(api_key: Optional[str] = None) -> OpenAI:
    """
    Create an OpenAI client for translation API calls.
    Provider: OpenAI - api.openai.com
    """
    key = api_key or os.environ.get("OPENAI_API_KEY", "")
    if not key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return OpenAI(api_key=key)


def translate_compliance_note(
    text: str,
    source_language: str = "en",
    target_language: str = "es",
    api_key: Optional[str] = None,
    model: str = OPENAI_TRANSLATION_MODEL,
) -> TranslationResponse:
    """
    Translate an encryption or compliance note using OpenAI Chat Completions API.

    Provider: OpenAI Chat Completions API - api.openai.com
    Model: gpt-4o-mini

    Args:
        text: The compliance or encryption note text to translate.
        source_language: Source language code (default: en).
        target_language: Target language code (default: es).
        api_key: Optional OpenAI API key override.
        model: Model to use for translation (default: gpt-4o-mini).

    Returns:
        TranslationResponse with translated text.
    """
    request = TranslationRequest(
        text=text,
        source_language=source_language,
        target_language=target_language,
    )
    normalized_text = request.to_normalized_text()

    if not normalized_text:
        raise ValueError("Note text cannot be empty")

    source_name = SUPPORTED_LANGUAGES.get(source_language, source_language)
    target_name = SUPPORTED_LANGUAGES.get(target_language, target_language)

    client = create_openai_client(api_key)

    system_prompt = (
        f"You are a professional translator specializing in cybersecurity, "
        f"encryption, and regulatory compliance terminology. "
        f"Translate the following text from {source_name} to {target_name}. "
        f"Preserve all technical terms, compliance framework references "
        f"(e.g., SOC 2, PCI DSS, GDPR, HIPAA, NIST, FIPS 140-2), "
        f"and encryption algorithm names (e.g., AES-256-GCM, RSA-4096, "
        f"ECDSA, SHA-256) without translation. "
        f"Return only the translated text without explanations."
    )

    try:
        logger.info(
            "Translating compliance note from %s to %s with OpenAI model %s",
            source_language, target_language, model,
        )

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": normalized_text},
            ],
            temperature=0.3,
            max_tokens=1024,
        )

        translated = response.choices[0].message.content.strip()

        result = TranslationResponse(
            translated_text=translated,
            source_language=source_language,
            target_language=target_language,
        )

        logger.info("Translation complete: %d chars input -> %d chars output",
                     len(normalized_text), len(translated))
        return result

    except Exception as e:
        logger.error("OpenAI translation error: %s", e)
        raise


def translate_compliance_notes_batch(
    notes: List[Dict[str, str]],
    source_language: str = "en",
    target_language: str = "es",
    api_key: Optional[str] = None,
    model: str = OPENAI_TRANSLATION_MODEL,
) -> List[TranslationResponse]:
    """
    Translate multiple compliance notes using OpenAI Chat Completions API.

    Provider: OpenAI Chat Completions API - api.openai.com
    Model: gpt-4o-mini

    Args:
        notes: List of dicts with 'text' key, optionally 'id' key.
        source_language: Source language code.
        target_language: Target language code.
        api_key: Optional API key override.
        model: Model to use.

    Returns:
        List of TranslationResponse objects.
    """
    results = []
    for note in notes:
        text = note.get("text", "")
        try:
            result = translate_compliance_note(
                text=text,
                source_language=source_language,
                target_language=target_language,
                api_key=api_key,
                model=model,
            )
            results.append(result)
        except Exception as e:
            logger.error("Failed to translate note: %s", e)
            results.append(
                TranslationResponse(
                    translated_text=f"[Translation Error: {e}]",
                    source_language=source_language,
                    target_language=target_language,
                )
            )
    return results


def translate_with_context(
    text: str,
    source_language: str = "en",
    target_language: str = "es",
    context_notes: Optional[List[str]] = None,
    api_key: Optional[str] = None,
    model: str = OPENAI_TRANSLATION_MODEL,
) -> TranslationResponse:
    """
    Translate a compliance note with additional context for better accuracy.

    Provider: OpenAI Chat Completions API - api.openai.com
    Model: gpt-4o-mini

    Args:
        text: The note text to translate.
        source_language: Source language code.
        target_language: Target language code.
        context_notes: Optional list of related context notes.
        api_key: Optional API key override.
        model: Model to use.

    Returns:
        TranslationResponse with translated text.
    """
    source_name = SUPPORTED_LANGUAGES.get(source_language, source_language)
    target_name = SUPPORTED_LANGUAGES.get(target_language, target_language)

    client = create_openai_client(api_key)

    context_section = ""
    if context_notes:
        context_section = (
            "\nRelated context for reference:\n" +
            "\n".join(f"- {note}" for note in context_notes)
        )

    system_prompt = (
        f"You are a professional translator specializing in cybersecurity, "
        f"encryption, and regulatory compliance terminology. "
        f"Translate the following text from {source_name} to {target_name}. "
        f"Use the related context (if provided) to ensure consistent "
        f"terminology across related documents. "
        f"Preserve all technical terms, compliance framework references, "
        f"and encryption algorithm names without translation. "
        f"Return only the translated text.{context_section}"
    )

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text},
            ],
            temperature=0.3,
            max_tokens=1024,
        )

        translated = response.choices[0].message.content.strip()

        return TranslationResponse(
            translated_text=translated,
            source_language=source_language,
            target_language=target_language,
        )

    except Exception as e:
        logger.error("OpenAI context-aware translation error: %s", e)
        raise


def generate_bilingual_report(
    original_note: str,
    translations: List[TranslationResponse],
) -> str:
    """
    Generate a bilingual compliance report with original and translations.

    Args:
        original_note: The original note text.
        translations: List of TranslationResponse objects.

    Returns:
        Formatted bilingual report string.
    """
    lines = [
        "=" * 60,
        "COMPLIANCE NOTE - BILINGUAL REPORT",
        "=" * 60,
        "",
        f"Original: {original_note}",
        "",
    ]

    for t in translations:
        lang_name = SUPPORTED_LANGUAGES.get(t.target_language, t.target_language)
        lines.append(f"--- {lang_name} ({t.target_language}) ---")
        lines.append(t.translated_text)
        lines.append("")

    lines.append("=" * 60)
    return "\n".join(lines)


if __name__ == "__main__":
    sample_note = (
        "The encryption key for customer PII data has been rotated per "
        "NIST SP 800-57 guidelines. AES-256-GCM with RSA-4096 key wrapping "
        "is in compliance with SOC 2 Type II requirements."
    )
    result = translate_compliance_note(sample_note, target_language="es")
    print(result.to_dict())
