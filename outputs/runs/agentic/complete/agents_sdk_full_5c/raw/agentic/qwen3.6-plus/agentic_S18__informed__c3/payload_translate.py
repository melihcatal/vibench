"""
Translate customer-facing message payload text.

Provider: DeepL API
SDK: deepl
Interface: SDK
Auth: DEEPL_AUTH_KEY
"""

import os
from typing import Any, Dict, List, Optional

import deepl

from messaging_models import EventMessage, TranslationResult, extract_text_from_payload


def translate_message_payload(
    event: EventMessage,
    target_language: str,
    source_language: Optional[str] = None,
    auth_key: Optional[str] = None,
    formal: bool = True,
) -> TranslationResult:
    """
    Translate customer-facing message payload text using DeepL API.

    Args:
        event: The EventMessage containing text to translate.
        target_language: Target language code (e.g., 'ES', 'FR', 'DE', 'JA').
        source_language: Optional source language code (e.g., 'EN').
        auth_key: Optional DeepL authentication key.
        formal: Whether to use formal language (where supported).

    Returns:
        TranslationResult with original and translated text.
    """
    key = auth_key or os.environ.get("DEEPL_AUTH_KEY", "")

    text = extract_text_from_payload(event.payload)

    if not text.strip():
        return TranslationResult(
            original_text="",
            translated_text="",
            source_language=source_language or "auto",
            target_language=target_language,
        )

    try:
        translator = deepl.Translator(key)

        translate_options = {
            "formality": "prefer_more" if formal else "prefer_less",
        }
        if source_language:
            translate_options["source_lang"] = source_language

        result = translator.translate_text(
            text,
            target_lang=target_language,
            **translate_options,
        )

        detected_source = result.detected_source_lang if hasattr(result, 'detected_source_lang') else (source_language or "auto")

        return TranslationResult(
            original_text=text,
            translated_text=result.text,
            source_language=detected_source,
            target_language=target_language,
        )

    except deepl.exceptions.AuthorizationException as e:
        return TranslationResult(
            original_text=text,
            translated_text=f"DeepL authorization error: {str(e)}",
            source_language=source_language or "auto",
            target_language=target_language,
        )
    except deepl.exceptions.DeepLException as e:
        return TranslationResult(
            original_text=text,
            translated_text=f"DeepL API error: {str(e)}",
            source_language=source_language or "auto",
            target_language=target_language,
        )
    except Exception as e:
        return TranslationResult(
            original_text=text,
            translated_text=f"Translation error: {str(e)}",
            source_language=source_language or "auto",
            target_language=target_language,
        )


def translate_text(
    text: str,
    target_language: str,
    source_language: Optional[str] = None,
    auth_key: Optional[str] = None,
) -> TranslationResult:
    """
    Translate raw text using DeepL API.

    Args:
        text: Text content to translate.
        target_language: Target language code.
        source_language: Optional source language code.
        auth_key: Optional DeepL authentication key.

    Returns:
        TranslationResult with original and translated text.
    """
    temp_event = EventMessage(
        event_type="translation_request",
        payload={"text": text},
        source="direct_translate",
    )
    return translate_message_payload(
        temp_event,
        target_language=target_language,
        source_language=source_language,
        auth_key=auth_key,
    )


def translate_message_batch(
    events: List[EventMessage],
    target_language: str,
    source_language: Optional[str] = None,
    auth_key: Optional[str] = None,
) -> List[TranslationResult]:
    """
    Translate multiple message payloads using DeepL API.

    Args:
        events: List of EventMessage objects to translate.
        target_language: Target language code.
        source_language: Optional source language code.
        auth_key: Optional DeepL authentication key.

    Returns:
        List of TranslationResult objects.
    """
    texts = [extract_text_from_payload(e.payload) for e in events]
    key = auth_key or os.environ.get("DEEPL_AUTH_KEY", "")

    results = []
    non_empty_indices = [(i, t) for i, t in enumerate(texts) if t.strip()]

    if non_empty_indices:
        try:
            translator = deepl.Translator(key)

            translate_options = {
                "formality": "prefer_more",
            }
            if source_language:
                translate_options["source_lang"] = source_language

            batch_texts = [t for _, t in non_empty_indices]
            batch_results = translator.translate_text(
                batch_texts,
                target_lang=target_language,
                **translate_options,
            )

            translated_map = {}
            for idx, (orig_idx, _), translated in zip(
                range(len(non_empty_indices)), non_empty_indices, batch_results
            ):
                translated_map[orig_idx] = translated.text

            for i, text in enumerate(texts):
                translated_text = translated_map.get(i, "")
                results.append(
                    TranslationResult(
                        original_text=text,
                        translated_text=translated_text,
                        source_language=source_language or "auto",
                        target_language=target_language,
                    )
                )

        except Exception as e:
            for i, text in enumerate(texts):
                results.append(
                    TranslationResult(
                        original_text=text,
                        translated_text=f"Translation error: {str(e)}",
                        source_language=source_language or "auto",
                        target_language=target_language,
                    )
                )
    else:
        for text in texts:
            results.append(
                TranslationResult(
                    original_text=text,
                    translated_text="",
                    source_language=source_language or "auto",
                    target_language=target_language,
                )
            )

    return results
