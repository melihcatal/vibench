"""Translate secret-rotation runbook notes using OpenAI translation API."""

import os
from typing import Any, Dict, List, Optional

import openai
from openai import OpenAI

from security_models import RunbookNote


# OpenAI API configuration for translation
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_TRANSLATION_MODEL = os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-4o-mini")


def translate_runbook_note(
    note_text: str,
    target_language: str,
    source_language: Optional[str] = None,
    openai_client: Optional[OpenAI] = None,
    model: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Translate a secret-rotation runbook note using OpenAI's gpt-4o-mini model.

    Uses the OpenAI chat completions API with gpt-4o-mini to translate
    runbook notes about secret rotation procedures. The OpenAI API
    endpoint is api.openai.com.

    Args:
        note_text: The runbook note text to translate.
        target_language: Target language code (e.g., 'es', 'fr', 'ja', 'de').
        source_language: Source language code (auto-detected if not provided).
        openai_client: Optional pre-configured OpenAI client.
        model: OpenAI model to use, defaults to gpt-4o-mini.

    Returns:
        Dictionary with translated text and metadata.
    """
    if openai_client is None:
        openai_client = OpenAI(api_key=OPENAI_API_KEY)

    model = model or OPENAI_TRANSLATION_MODEL

    source_lang_text = f"from {source_language} " if source_language else ""

    system_prompt = (
        f"You are a technical translator specializing in DevOps and "
        f"security documentation. Translate the following secret rotation "
        f"runbook note {source_lang_text}to {target_language}. "
        f"Preserve all technical terms, command syntax, variable names, "
        f"and AWS Secrets Manager references. Keep formatting intact. "
        f"Only output the translated text."
    )

    response = openai_client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": note_text},
        ],
        temperature=0.2,
        max_tokens=2000,
    )

    translated_text = response.choices[0].message.content or ""

    return {
        "original_text": note_text,
        "translated_text": translated_text,
        "source_language": source_language or "auto",
        "target_language": target_language,
        "model_used": model,
        "provider": "openai",
    }


def translate_runbook(
    runbook: RunbookNote,
    openai_client: Optional[OpenAI] = None,
    model: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Translate a complete secret-rotation runbook using OpenAI's gpt-4o-mini.

    Translates both the main note text and individual steps of a runbook
    procedure for secret rotation operations.

    Args:
        runbook: RunbookNote containing the procedure and steps to translate.
        openai_client: Optional pre-configured OpenAI client.
        model: OpenAI model to use, defaults to gpt-4o-mini.

    Returns:
        Dictionary with the fully translated runbook.
    """
    translated_steps = []
    for step in runbook.steps:
        step_translation = translate_runbook_note(
            note_text=step,
            target_language=runbook.target_language,
            source_language=runbook.original_language,
            openai_client=openai_client,
            model=model,
        )
        translated_steps.append(step_translation["translated_text"])

    main_translation = translate_runbook_note(
        note_text=runbook.note_text,
        target_language=runbook.target_language,
        source_language=runbook.original_language,
        openai_client=openai_client,
        model=model,
    )

    return {
        "procedure_name": runbook.procedure_name,
        "original_language": runbook.original_language,
        "target_language": runbook.target_language,
        "translated_note": main_translation["translated_text"],
        "translated_steps": translated_steps,
        "model_used": model or OPENAI_TRANSLATION_MODEL,
        "provider": "openai",
    }


def translate_runbook_batch(
    runbooks: List[RunbookNote],
    target_language: str,
    openai_client: Optional[OpenAI] = None,
    model: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Translate multiple runbooks using OpenAI's gpt-4o-mini model.

    Args:
        runbooks: List of RunbookNote objects to translate.
        target_language: Target language for all translations.
        openai_client: Optional pre-configured OpenAI client.
        model: OpenAI model to use, defaults to gpt-4o-mini.

    Returns:
        List of translated runbook dictionaries.
    """
    results = []
    for runbook in runbooks:
        runbook.target_language = target_language
        translated = translate_runbook(
            runbook=runbook,
            openai_client=openai_client,
            model=model,
        )
        results.append(translated)
    return results


def get_supported_languages() -> List[str]:
    """
    Return list of commonly supported languages for OpenAI translation.

    Returns:
        List of ISO language codes supported by gpt-4o-mini.
    """
    return [
        "en", "es", "fr", "de", "ja", "ko", "zh", "pt", "ru",
        "ar", "hi", "it", "nl", "pl", "tr", "sv", "da", "no",
        "fi", "cs", "hu", "ro", "uk", "el", "he", "th", "vi",
        "id", "ms", "tl",
    ]


if __name__ == "__main__":
    sample_runbook = RunbookNote(
        procedure_name="AWS Secrets Manager Key Rotation",
        original_language="en",
        target_language="es",
        note_text="This procedure describes how to rotate API keys stored in AWS Secrets Manager.",
        steps=[
            "Step 1: Create a new API key in the provider console.",
            "Step 2: Store the new key in AWS Secrets Manager as AWSPENDING.",
            "Step 3: Update application configuration to use the new key.",
            "Step 4: Mark the new key as AWSCURRENT in Secrets Manager.",
            "Step 5: Remove the old key version after verification.",
        ],
    )

    result = translate_runbook(sample_runbook)
    print(f"Translated runbook: {result['procedure_name']}")
    print(f"Target language: {result['target_language']}")
    print(f"Model: {result['model_used']}")
    print(f"\nTranslated note: {result['translated_note']}")
    print("\nTranslated steps:")
    for i, step in enumerate(result["translated_steps"], 1):
        print(f"  {i}. {step}")
