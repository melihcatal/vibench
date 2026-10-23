"""Translate support-visible log messages for another locale using OpenAI and Datadog.

Provider (log query): Datadog Logs API v2
- Endpoint: POST https://api.datadoghq.com/api/v2/logs/events/search
- SDK: datadog-api-client (datadog_api_client.v2.api.logs_api.LogsApi)

Provider (translation): OpenAI Chat Completions API
- Model: gpt-4o
- Endpoint: https://api.openai.com/v1/chat/completions
- SDK: openai
"""

import os
import json
from typing import Optional

from openai import OpenAI
from fetch_recent_logs import fetch_recent_logs
from observability_models import LogQueryResponse
from observability_client import DatadogObservabilityClient


OPENAI_MODEL = "gpt-4o"


def translate_log_messages(
    service: str,
    target_locale: str = "es",
    hours: int = 1,
    limit: int = 30,
    client: Optional[DatadogObservabilityClient] = None,
    openai_client: Optional[OpenAI] = None,
) -> list[dict]:
    """Fetch log messages from Datadog and translate them for support visibility.

    Steps:
    1. Fetch recent logs from Datadog Logs API v2 for the given service.
    2. Extract log message text from entries.
    3. Batch-translate messages using OpenAI gpt-4o to the target locale.
    4. Return translated messages paired with originals.

    Args:
        service: The service name to fetch logs for.
        target_locale: Target language/locale code (e.g. "es", "fr", "ja", "de").
        hours: Number of recent hours to search.
        limit: Maximum number of log entries to translate.
        client: Optional pre-configured DatadogObservabilityClient.
        openai_client: Optional pre-configured OpenAI client.

    Returns:
        List of dicts with original message, translated message, and metadata.
    """
    if openai_client is None:
        openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))

    response: LogQueryResponse = fetch_recent_logs(
        service=service,
        hours=hours,
        limit=limit,
        client=client,
    )

    messages = []
    for log in response.logs:
        msg_text = log.get("message", "").strip()
        if msg_text:
            messages.append({
                "timestamp": log.get("date", ""),
                "message": msg_text,
                "service": log.get("service", ""),
                "status": log.get("status", ""),
                "hostname": log.get("hostname", ""),
            })

    if not messages:
        return []

    locale_name = _locale_name(target_locale)
    translations = _batch_translate(openai_client, messages, target_locale, locale_name)
    return translations


def _locale_name(code: str) -> str:
    """Map locale codes to human-readable language names for the translation prompt."""
    locale_map = {
        "es": "Spanish",
        "fr": "French",
        "de": "German",
        "ja": "Japanese",
        "zh": "Chinese",
        "ko": "Korean",
        "pt": "Portuguese",
        "it": "Italian",
        "ru": "Russian",
        "ar": "Arabic",
        "hi": "Hindi",
    }
    return locale_map.get(code, code)


def _batch_translate(
    openai_client: OpenAI,
    messages: list[dict],
    target_locale: str,
    locale_name: str,
) -> list[dict]:
    """Translate a batch of log messages using OpenAI gpt-4o.

    Messages are sent in a single prompt for efficiency, and the response
    is parsed back into paired translations.
    """
    lines = []
    for i, entry in enumerate(messages, 1):
        lines.append(f"{i}. {entry['message']}")
    message_list = "\n".join(lines)

    prompt = (
        f"Translate the following log messages to {locale_name} ({target_locale}). "
        "Preserve technical terms, variable names, and placeholders exactly. "
        "Return the translations in the same order, one per line, numbered 1 to N.\n\n"
        f"{message_list}"
    )

    response = openai_client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a technical translator specializing in software log messages. "
                    "Preserve all technical identifiers, error codes, and variable names."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
        max_tokens=2048,
    )

    translated_text = response.choices[0].message.content.strip()
    translated_lines = [
        line.lstrip("0123456789. ") for line in translated_text.split("\n") if line.strip()
    ]

    results = []
    for i, entry in enumerate(messages):
        translated = translated_lines[i] if i < len(translated_lines) else ""
        results.append({
            "original": entry["message"],
            "translated": translated,
            "locale": target_locale,
            "timestamp": entry["timestamp"],
            "service": entry["service"],
            "status": entry.get("status", ""),
            "model_used": OPENAI_MODEL,
        })
    return results


def main():
    """Entry point for translating log messages."""
    service = os.environ.get("LOG_SERVICE", "web-api")
    target_locale = os.environ.get("TRANSLATE_LOCALE", "es")
    hours = int(os.environ.get("TRANSLATE_HOURS", "1"))

    results = translate_log_messages(
        service=service,
        target_locale=target_locale,
        hours=hours,
    )
    print(json.dumps(results, indent=2, default=str, ensure_ascii=False))


if __name__ == "__main__":
    main()
