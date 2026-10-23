"""Translate support-visible log messages for another locale using Google Cloud Translation."""

import json
import os
from typing import List, Optional

from google.cloud import translate_v2 as translate

from observability_models import LogEntry


def translate_log_messages(
    log_messages: List[str],
    target_language: str = "es",
    source_language: Optional[str] = None,
    model: str = "nmt",
) -> dict:
    """Translate support-visible log messages using Google Cloud Translation.

    Uses the google-cloud-translate SDK with GOOGLE_APPLICATION_CREDENTIALS
    for authentication. The service supports the NMT (neural machine translation)
    model via the Cloud Translation v2 API.
    """
    client = translate.Client()

    translate_options = {
        "model": model,
        "target_language": target_language,
    }
    if source_language:
        translate_options["source_language"] = source_language

    results = client.translate(log_messages, **translate_options)

    translations = []
    for i, result in enumerate(results):
        translations.append({
            "index": i,
            "original": result.get("input", ""),
            "translated": result.get("translatedText", ""),
            "detected_source": result.get("detectedSourceLanguage", ""),
            "model": model,
        })

    return {
        "provider": "Google Cloud Translation",
        "target_language": target_language,
        "source_language": source_language,
        "model": model,
        "messages_translated": len(translations),
        "translations": translations,
    }


def translate_log_entries(
    log_entries: List[LogEntry],
    target_language: str = "es",
    source_language: Optional[str] = None,
) -> dict:
    """Extract messages from log entries and translate them for support review."""
    messages = [str(entry.message) for entry in log_entries if entry.message]
    return translate_log_messages(
        messages,
        target_language=target_language,
        source_language=source_language,
    )


def main():
    sample_messages = [
        "Database connection timeout after 30 seconds",
        "Failed to authenticate user: invalid credentials",
        "Request processed successfully in 245ms",
    ]

    result = translate_log_messages(
        sample_messages,
        target_language="es",
        model="nmt",
    )
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
