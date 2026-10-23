import os
from typing import Any, Dict, Optional

import openai
from openai import OpenAI

from security_models import (
    ComplianceTranslationRequest,
    ComplianceTranslationResponse,
)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_TRANSLATION_MODEL = os.environ.get("OPENAI_TRANSLATION_MODEL", "gpt-4o-mini")
OPENAI_API_BASE = os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1")


def get_openai_client() -> OpenAI:
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return OpenAI(
        api_key=OPENAI_API_KEY,
        base_url=OPENAI_API_BASE,
    )


def translate_compliance_notes(
    compliance_notes: str,
    target_language: str = "en",
    source_language: str = "auto",
    context: Optional[str] = None,
    model: str = OPENAI_TRANSLATION_MODEL,
) -> ComplianceTranslationResponse:
    client = get_openai_client()

    system_prompt = (
        "You are a professional translator specializing in cybersecurity, "
        "encryption, and compliance documentation. Translate the provided "
        "compliance notes accurately while preserving technical terminology. "
        "Maintain the formal tone appropriate for regulatory and audit contexts."
    )

    if context:
        system_prompt += f"\n\nAdditional context: {context}"

    lang_instruction = f"Translate the following compliance notes from {source_language} to {target_language}."
    if source_language == "auto":
        lang_instruction = f"Detect the language and translate the following compliance notes to {target_language}."

    user_prompt = f"{lang_instruction}\n\nCompliance Notes:\n{compliance_notes}"

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.1,
        max_tokens=2048,
    )

    translated_text = response.choices[0].message.content.strip()

    result = ComplianceTranslationResponse(
        translated_text=translated_text,
        source_language_detected=source_language,
        target_language=target_language,
        model=model,
    )
    return result


def translate_compliance_notes_with_glossary(
    compliance_notes: str,
    target_language: str = "en",
    glossary: Optional[Dict[str, str]] = None,
    context: Optional[str] = None,
    model: str = OPENAI_TRANSLATION_MODEL,
) -> ComplianceTranslationResponse:
    client = get_openai_client()

    system_prompt = (
        "You are a professional translator specializing in cybersecurity, "
        "encryption, and compliance documentation. Translate the provided "
        "compliance notes accurately while preserving technical terminology."
    )

    if glossary:
        glossary_entries = "\n".join(f"- {k}: {v}" for k, v in glossary.items())
        system_prompt += f"\n\nUse the following glossary for consistent terminology:\n{glossary_entries}"

    if context:
        system_prompt += f"\n\nAdditional context: {context}"

    user_prompt = f"Translate the following compliance notes to {target_language}:\n\n{compliance_notes}"

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.1,
        max_tokens=2048,
    )

    translated_text = response.choices[0].message.content.strip()

    result = ComplianceTranslationResponse(
        translated_text=translated_text,
        source_language_detected="auto",
        target_language=target_language,
        model=model,
    )
    return result


def batch_translate_compliance_notes(
    notes_list: list,
    target_language: str = "en",
    context: Optional[str] = None,
    model: str = OPENAI_TRANSLATION_MODEL,
) -> list:
    results = []
    for notes in notes_list:
        if isinstance(notes, ComplianceTranslationRequest):
            response = translate_compliance_notes(
                compliance_notes=notes.compliance_notes,
                target_language=notes.target_language,
                source_language=notes.source_language,
                context=notes.context or context,
                model=model,
            )
        else:
            response = translate_compliance_notes(
                compliance_notes=notes,
                target_language=target_language,
                context=context,
                model=model,
            )
        results.append(response)
    return results


def translate_and_format_compliance_report(
    compliance_notes: str,
    target_language: str = "en",
    format_as: str = "markdown",
    model: str = OPENAI_TRANSLATION_MODEL,
) -> Dict[str, Any]:
    client = get_openai_client()

    system_prompt = (
        "You are a professional translator specializing in cybersecurity "
        "and compliance documentation. Translate the provided compliance "
        f"notes to {target_language} and format the output as {format_as}. "
        "Preserve all technical terms, references, and regulatory citations."
    )

    user_prompt = (
        f"Translate and format the following compliance notes:\n\n{compliance_notes}"
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.1,
        max_tokens=4096,
    )

    translated_text = response.choices[0].message.content.strip()

    result = ComplianceTranslationResponse(
        translated_text=translated_text,
        source_language_detected="auto",
        target_language=target_language,
        model=model,
    )

    return {
        "translation": result.to_dict(),
        "format": format_as,
        "original_length": len(compliance_notes),
        "translated_length": len(translated_text),
    }
