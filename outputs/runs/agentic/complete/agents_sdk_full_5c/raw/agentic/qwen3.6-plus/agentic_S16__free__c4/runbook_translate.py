"""Translate secret-rotation runbook notes using OpenAI GPT-4o model."""

import os
from typing import Optional
import openai
from openai import OpenAI
from security_models import SecretError


# OpenAI provider configuration
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_CHAT_MODEL = os.environ.get("OPENAI_CHAT_MODEL", "gpt-4o")
OPENAI_TEMPERATURE = float(os.environ.get("OPENAI_TEMPERATURE", "0.2"))


def _get_openai_client() -> OpenAI:
    """Create an OpenAI client for chat completions."""
    if not OPENAI_API_KEY:
        raise SecretError(
            secret_id="openai_config",
            message="OPENAI_API_KEY environment variable is not set",
            error_code="MISSING_API_KEY",
            provider="openai",
        )
    return OpenAI(api_key=OPENAI_API_KEY)


def translate_runbook_note(
    note_text: str,
    target_language: str = "en",
    source_language: str = "auto",
) -> dict:
    """Translate a secret-rotation runbook note using OpenAI gpt-4o model.

    Uses the OpenAI chat completions API with model gpt-4o to translate
    runbook notes related to secret rotation procedures.

    Args:
        note_text: The runbook note text to translate.
        target_language: Target language code (e.g., 'en', 'es', 'fr', 'ja', 'zh').
        source_language: Source language code, or 'auto' for auto-detection.

    Returns:
        Dict with:
            - original_text: the input note text
            - translated_text: the translated result
            - source_language: detected or specified source language
            - target_language: the target language code
            - model: the OpenAI model used (gpt-4o)
            - provider: "openai"
    """
    system_prompt = (
        "You are a technical translator specializing in security operations "
        "and secret management runbooks. Translate the following runbook note "
        "about secret rotation procedures accurately, preserving technical terms "
        "like AWS Secrets Manager, rotation Lambda, AWSCURRENT, AWSPENDING, "
        "and API keys. Keep the translation professional and precise."
    )

    if source_language != "auto":
        user_prompt = (
            f"Translate the following secret-rotation runbook note from "
            f"{source_language} to {target_language}:\n\n{note_text}"
        )
    else:
        user_prompt = (
            f"Detect the language of the following secret-rotation runbook note "
            f"and translate it to {target_language}:\n\n{note_text}\n\n"
            f"First state the detected source language, then provide the translation."
        )

    client = _get_openai_client()
    try:
        response = client.chat.completions.create(
            model=OPENAI_CHAT_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=OPENAI_TEMPERATURE,
        )
        translated = response.choices[0].message.content.strip()
        return {
            "original_text": note_text,
            "translated_text": translated,
            "source_language": source_language,
            "target_language": target_language,
            "model": OPENAI_CHAT_MODEL,
            "provider": "openai",
        }
    except openai.APIError as exc:
        raise SecretError(
            secret_id="runbook_translation",
            message=f"OpenAI chat completions API error (gpt-4o): {exc}",
            error_code="OPENAI_API_ERROR",
            provider="openai",
        )


def translate_runbook_notes(
    notes: list[str],
    target_language: str = "en",
) -> list[dict]:
    """Translate multiple secret-rotation runbook notes via OpenAI gpt-4o.

    Args:
        notes: List of runbook note strings to translate.
        target_language: Target language code.

    Returns:
        List of translation result dicts.
    """
    results = []
    for note in notes:
        result = translate_runbook_note(note, target_language=target_language)
        results.append(result)
    return results


def translate_runbook_batch(
    notes: list[str],
    target_language: str = "en",
) -> str:
    """Translate multiple runbook notes in a single OpenAI gpt-4o call.

    More cost-effective for translating many notes at once.

    Args:
        notes: List of runbook note strings.
        target_language: Target language code.

    Returns:
        Combined translated text with numbered entries.
    """
    numbered_notes = "\n".join(
        f"[{i+1}] {note}" for i, note in enumerate(notes)
    )

    system_prompt = (
        "You are a technical translator for security operations runbooks. "
        "Translate the numbered secret-rotation runbook notes below to "
        f"{target_language}. Preserve the numbering and technical terms "
        "like AWS Secrets Manager, rotation stages, and credential types."
    )

    client = _get_openai_client()
    try:
        response = client.chat.completions.create(
            model=OPENAI_CHAT_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Translate these notes:\n\n{numbered_notes}"},
            ],
            temperature=OPENAI_TEMPERATURE,
        )
        return response.choices[0].message.content.strip()
    except openai.APIError as exc:
        raise SecretError(
            secret_id="runbook_batch_translation",
            message=f"OpenAI chat completions API error (gpt-4o): {exc}",
            error_code="OPENAI_API_ERROR",
            provider="openai",
        )


if __name__ == "__main__":
    sample_note = (
        "Rotate the AWS Secrets Manager secret 'prod/api/key' by invoking "
        "the rotation Lambda. Verify AWSPENDING becomes AWSCURRENT after "
        "the rotation completes. Update the API key in the service config."
    )
    result = translate_runbook_note(sample_note, target_language="es")
    print(f"Translated with {result['model']}: {result['translated_text'][:100]}...")
