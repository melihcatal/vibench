"""
[LATER-STEP] log_message_translate.py

Translates support-visible log messages for another locale using the Azure OpenAI Service.
Uses the openai Python SDK configured to target Azure OpenAI endpoints.
"""

import json
import os
import sys
from typing import Dict, Any, List, Optional

from openai import AzureOpenAI

from observability_models import LogEntry


AZURE_OPENAI_ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT", "")
AZURE_OPENAI_API_KEY = os.environ.get("AZURE_OPENAI_API_KEY", "")
AZURE_OPENAI_API_VERSION = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-06-01")
AZURE_TRANSLATION_DEPLOYMENT = os.environ.get("AZURE_TRANSLATION_DEPLOYMENT", "gpt-4o-mini")


def translate_log_message(
    log_message: str,
    target_language: str = "es",
    deployment: str | None = None,
) -> Dict[str, Any]:
    """
    Translate a log message for support visibility into another locale.

    Args:
        log_message: The original log message text.
        target_language: Target locale code (e.g., es, fr, ja, de).
        deployment: Azure OpenAI deployment name for translation.

    Returns:
        Dict with the translated message and metadata.
    """
    deployment_name = deployment or AZURE_TRANSLATION_DEPLOYMENT

    system_prompt = (
        "You are a technical translator specializing in software logs and error messages. "
        "Translate the following log message into the target language. "
        "Preserve any technical identifiers, codes, timestamps, and file paths exactly. "
        "Do not translate variable names, stack trace references, or numeric IDs."
    )

    language_map = {
        "es": "Spanish",
        "fr": "French",
        "ja": "Japanese",
        "de": "German",
        "zh": "Chinese (Simplified)",
        "pt": "Portuguese",
        "ko": "Korean",
        "it": "Italian",
        "ru": "Russian",
        "ar": "Arabic",
    }
    lang_name = language_map.get(target_language, target_language)

    user_prompt = (
        f"Translate this log message into {lang_name} ({target_language}):\n\n"
        f"{log_message}"
    )

    try:
        client = AzureOpenAI(
            api_key=AZURE_OPENAI_API_KEY,
            api_version=AZURE_OPENAI_API_VERSION,
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
        )

        completion = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.3,
            max_tokens=512,
        )

        translated_text = completion.choices[0].message.content or ""

        return {
            "status": "translated",
            "original": log_message,
            "translated": translated_text,
            "target_language": target_language,
            "language_name": lang_name,
            "model_used": f"Azure OpenAI deployment: {deployment_name}",
            "deployment_endpoint": AZURE_OPENAI_ENDPOINT[:40] + "...",
        }

    except Exception as exc:
        return {
            "status": "error",
            "message": f"Failed to translate log message with Azure OpenAI: {exc}",
            "original": log_message,
            "target_language": target_language,
        }


def translate_log_entries(
    entries: List[LogEntry],
    target_language: str = "es",
    deployment: str | None = None,
) -> Dict[str, Any]:
    """
    Translate multiple log entries for support visibility.

    Args:
        entries: List of LogEntry objects to translate.
        target_language: Target locale code.
        deployment: Azure OpenAI deployment name.

    Returns:
        Dict with batch translation results.
    """
    results = []
    deployment_name = deployment or AZURE_TRANSLATION_DEPLOYMENT

    for entry in entries:
        translation_result = translate_log_message(
            entry.message,
            target_language=target_language,
            deployment=deployment_name,
        )
        translation_result["entry_service"] = entry.service
        translation_result["entry_status"] = entry.status
        translation_result["entry_timestamp"] = entry.timestamp
        results.append(translation_result)

    return {
        "status": "batch_complete",
        "total_translated": len(results),
        "target_language": target_language,
        "results": results,
    }


def main() -> None:
    """CLI entry point for translating log messages with Azure OpenAI."""
    if len(sys.argv) < 3:
        print("Usage: log_message_translate.py <log_message> <target_language>")
        sys.exit(1)

    message = sys.argv[1]
    language = sys.argv[2]
    result = translate_log_message(message, target_language=language)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
