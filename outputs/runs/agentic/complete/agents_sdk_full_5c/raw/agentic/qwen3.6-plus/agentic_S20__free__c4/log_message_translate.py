"""
Translate support-visible log messages for another locale.

Uses the OpenAI Chat Completions API (api.openai.com) via the openai
Python SDK with the gpt-4o-mini model to translate log messages
into a target locale for support team review.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional

import openai
from openai import OpenAI

from observability_models import (
    LogQueryFilter,
    LogEntry,
    QueryResult,
)
from observability_client import query_logs

OPENAI_API_HOST = "https://api.openai.com/v1"
OPENAI_TRANSLATION_MODEL = "gpt-4o-mini"


def translate_log_message(
    message: str,
    target_locale: str = "es",
    source_locale: str = "en",
    model: str = OPENAI_TRANSLATION_MODEL,
) -> Dict[str, Any]:
    """Translate a single log message to a target locale using OpenAI.

    Uses the OpenAI GPT-4o-mini model at api.openai.com to translate
    log message text while preserving technical terms and identifiers.

    Args:
        message: The log message text to translate.
        target_locale: Target locale code (e.g., 'es', 'fr', 'ja').
        source_locale: Source locale code (default 'en').
        model: OpenAI model to use for translation.

    Returns:
        Dict with original message, translation, and metadata.
    """
    openai_client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY", ""),
        base_url=OPENAI_API_HOST,
    )

    system_prompt = (
        f"You are a professional translator specializing in technical and "
        f"software engineering content. Translate the provided log message "
        f"from {source_locale} to {target_locale}. "
        f"Preserve technical identifiers, error codes, HTTP status codes, "
        f"IP addresses, UUIDs, and any structured data formats. "
        f"Only output the translated text, nothing else."
    )

    response = openai_client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message},
        ],
        temperature=0.2,
        max_tokens=512,
    )

    translated_text = response.choices[0].message.content or ""

    return {
        "model": model,
        "provider": "openai",
        "provider_endpoint": OPENAI_API_HOST,
        "source_locale": source_locale,
        "target_locale": target_locale,
        "original_message": message,
        "translated_message": translated_text.strip(),
        "model_used": response.model,
    }


def translate_recent_logs(
    target_locale: str = "es",
    service: Optional[str] = None,
    time_window_minutes: int = 30,
    limit: int = 10,
    model: str = OPENAI_TRANSLATION_MODEL,
) -> Dict[str, Any]:
    """Fetch recent error logs from Datadog and translate their messages.

    Queries api.datadoghq.com via the datadog-api-client SDK for recent
    error logs, then translates each message using OpenAI GPT-4o-mini
    for support team review in another locale.
    """
    now = datetime.now(timezone.utc)
    time_from = now - timedelta(minutes=time_window_minutes)

    filter_fields = {"status": "error"}
    if service:
        filter_fields["service"] = service

    filter_query = LogQueryFilter(
        query="status:error",
        time_from=time_from,
        time_to=now,
        limit=limit,
        filter_fields=filter_fields,
    )

    log_result: QueryResult = query_logs(filter_query)

    translations = []
    for entry in log_result.entries:
        if entry.message:
            translation = translate_log_message(
                message=entry.message,
                target_locale=target_locale,
                model=model,
            )
            translation["log_id"] = entry.id
            translation["log_timestamp"] = entry.timestamp
            translation["log_service"] = entry.service
            translations.append(translation)

    return {
        "target_locale": target_locale,
        "model": model,
        "provider": "openai",
        "total_translated": len(translations),
        "source": "datadog",
        "translations": translations,
    }


def main() -> None:
    """CLI entry point for translating log messages."""
    message = os.environ.get("LOG_MESSAGE", "Connection timeout on database query")
    target_locale = os.environ.get("TARGET_LOCALE", "es")
    model = os.environ.get("OPENAI_MODEL", OPENAI_TRANSLATION_MODEL)

    result = translate_log_message(
        message=message,
        target_locale=target_locale,
        model=model,
    )
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
