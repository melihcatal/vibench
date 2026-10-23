"""Translate customer-facing message payload text.

Uses OpenAI Chat Completions API as the concrete external provider for translation.
"""

import os
from typing import Any, Dict, Optional

from openai import OpenAI

from messaging_models import EventMessage, MessageResponse


OPENAI_MODEL_ID = os.environ.get("OPENAI_TRANSLATION_MODEL", "gpt-4o-mini")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")


def _get_openai_client() -> OpenAI:
    """Create and return an OpenAI client for translation."""
    return OpenAI(api_key=OPENAI_API_KEY)


def _extract_text_from_payload(payload: Dict[str, Any]) -> str:
    """Extract the primary text content from a message payload."""
    for key in ("text", "message", "content", "body", "description"):
        val = payload.get(key)
        if val and isinstance(val, str):
            return val
    return str(payload)


def translate_message_payload(
    event: EventMessage,
    target_language: str = "en",
    source_language: Optional[str] = None,
    model: Optional[str] = None,
) -> MessageResponse:
    """Translate customer-facing message payload text using OpenAI.

    Args:
        event: The EventMessage containing the payload to translate.
        target_language: Target language code (e.g., 'en', 'es', 'fr', 'de').
        source_language: Optional source language code for better accuracy.
        model: The OpenAI model ID to use for translation.

    Returns:
        MessageResponse with translated text in details.
    """
    model_id = model or OPENAI_MODEL_ID
    text_to_translate = _extract_text_from_payload(event.payload)

    try:
        client = _get_openai_client()

        lang_instruction = f"Translate the following text to {target_language}."
        if source_language:
            lang_instruction = (
                f"Translate the following text from {source_language} to {target_language}."
            )

        system_prompt = (
            "You are a professional translator. Translate the provided text accurately "
            "while preserving the original meaning, tone, and formatting. "
            "Return only the translated text with no additional commentary."
        )

        response = client.chat.completions.create(
            model=model_id,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"{lang_instruction}\n\n{text_to_translate}"},
            ],
            temperature=0.3,
            max_tokens=1000,
        )

        translated_text = response.choices[0].message.content.strip()

        return MessageResponse(
            success=True,
            event_id=event.event_id,
            details={
                "original_text": text_to_translate,
                "translated_text": translated_text,
                "target_language": target_language,
                "source_language": source_language,
                "model": model_id,
                "provider": "openai",
            },
        )
    except Exception as exc:
        return MessageResponse(
            success=False,
            event_id=event.event_id,
            error=str(exc),
            details={
                "target_language": target_language,
                "provider": "openai",
                "model": model_id,
            },
        )


def translate_text(
    text: str,
    target_language: str = "en",
    source_language: Optional[str] = None,
    model: Optional[str] = None,
) -> MessageResponse:
    """Translate raw text using OpenAI.

    Args:
        text: The text to translate.
        target_language: Target language code.
        source_language: Optional source language code.
        model: The OpenAI model ID to use.

    Returns:
        MessageResponse with translated text.
    """
    event = EventMessage(
        event_type="translation_request",
        payload={"text": text},
    )
    return translate_message_payload(
        event=event,
        target_language=target_language,
        source_language=source_language,
        model=model,
    )
