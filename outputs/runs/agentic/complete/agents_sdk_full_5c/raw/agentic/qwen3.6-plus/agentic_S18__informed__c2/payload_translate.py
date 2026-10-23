"""
Translate customer-facing message payload text using DeepL API.

Uses the deepl SDK to translate text between supported languages
for international message delivery.
Requires DEEPL_AUTH_KEY environment variable for authentication.
"""

import os
import json
from typing import Optional

import deepl


class TranslationResult:
    """Result of a translation operation."""

    def __init__(self):
        self.original_text: str = ""
        self.translated_text: str = ""
        self.source_language: str = ""
        self.target_language: str = ""
        self.success: bool = False
        self.error: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "original_text": self.original_text,
            "translated_text": self.translated_text,
            "source_language": self.source_language,
            "target_language": self.target_language,
            "success": self.success,
            "error": self.error,
        }


def translate_payload(
    text: str,
    target_language: str = "ES",
    source_language: Optional[str] = None,
    auth_key: Optional[str] = None,
) -> TranslationResult:
    """
    Translate customer-facing message payload text using DeepL API.

    Args:
        text: The text to translate.
        target_language: Target language code (e.g., 'ES', 'FR', 'DE', 'JA', 'ZH').
        source_language: Source language code (None for auto-detect).
        auth_key: DeepL authentication key.

    Returns:
        TranslationResult with the translated text.
    """
    result = TranslationResult()
    result.original_text = text
    result.target_language = target_language

    try:
        key = auth_key or os.environ.get("DEEPL_AUTH_KEY", "")

        if not key:
            result.error = "DeepL authentication key not configured"
            return result

        translator = deepl.Translator(key)

        translate_options = {
            "target_lang": target_language,
        }
        if source_language:
            translate_options["source_lang"] = source_language

        translation = translator.translate_text(text, **translate_options)

        result.translated_text = translation.text
        result.source_language = translation.detected_source_lang or source_language or "auto"
        result.success = True

    except deepl.exceptions.AuthorizationException as e:
        result.error = f"DeepL authorization error: {str(e)}"
    except deepl.exceptions.DeepLException as e:
        result.error = f"DeepL API error: {str(e)}"
    except Exception as e:
        result.error = f"Unexpected error: {str(e)}"

    return result


def translate_payload_dict(
    payload: dict,
    target_language: str = "ES",
    text_keys: Optional[list] = None,
    auth_key: Optional[str] = None,
) -> dict:
    """
    Translate specific text fields in a message payload using DeepL API.

    Args:
        payload: Dictionary payload containing text to translate.
        target_language: Target language code.
        text_keys: List of keys to translate (defaults to 'message', 'text', 'content', 'body').
        auth_key: DeepL authentication key.

    Returns:
        New dictionary with translated text fields.
    """
    if text_keys is None:
        text_keys = ["message", "text", "content", "body", "description"]

    translated = payload.copy()

    for key in text_keys:
        if key in translated and isinstance(translated[key], str):
            translation = translate_payload(
                text=translated[key],
                target_language=target_language,
                auth_key=auth_key,
            )
            if translation.success:
                translated[key] = translation.translated_text
                translated[f"{key}_source_lang"] = translation.source_language

    return translated


if __name__ == "__main__":
    sample_text = "Your order has been shipped and will arrive in 3 business days."
    result = translate_payload(sample_text, target_language="FR")
    print(json.dumps(result.to_dict(), indent=2))
