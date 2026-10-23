"""Translate support-visible log messages for another locale using DeepL API."""

import json
import os
from typing import Optional

import deepl


DEEPL_AUTH_KEY = os.environ.get("DEEPL_AUTH_KEY", "")


def translate_log_message(
    message: str,
    target_language: str = "ES",
    source_language: Optional[str] = None,
) -> str:
    """Translate a log message string to a target locale using DeepL API.

    Uses the DeepL translate endpoint with the deep python SDK.
    Supported target languages: ES, FR, DE, JA, ZH, PT, etc.
    """
    translator = deepl.Translator(DEEPL_AUTH_KEY)

    kwargs = {"target_lang": target_language}
    if source_language:
        kwargs["source_lang"] = source_language

    result = translator.translate_text(message, **kwargs)
    return result.text


def translate_log_batch(
    messages: list[str],
    target_language: str = "ES",
    source_language: Optional[str] = None,
) -> list[dict]:
    """Batch translate multiple log messages to a target locale via DeepL API."""
    translator = deepl.Translator(DEEPL_AUTH_KEY)

    kwargs = {"target_lang": target_language}
    if source_language:
        kwargs["source_lang"] = source_language

    results = translator.translate_text(messages, **kwargs)
    return [
        {
            "original": msg,
            "translated": translated.text,
        }
        for msg, translated in zip(messages, results)
    ]


if __name__ == "__main__":
    sample_logs = [
        "Payment processing failed due to insufficient funds",
        "Database connection timeout after 30 seconds",
        "User session expired and has been refreshed automatically",
    ]
    translated = translate_log_batch(sample_logs, target_language="JA")
    print(json.dumps(translated, indent=2, ensure_ascii=False))
