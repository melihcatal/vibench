"""Translate support-visible log messages for another locale using OpenAI GPT-4."""

import os
from typing import Optional

from openai import OpenAI

from query_error_logs import query_error_logs
from observability_models import LogQueryResponse


def translate_log_messages(
    log_messages: list[str],
    target_language: str = "Spanish",
    service: str | None = None,
    time_range_minutes: int = 30,
    max_messages: int = 20,
) -> list[dict]:
    """
    Translate support-visible log messages to another locale.

    Uses the OpenAI GPT-4 model (openai package, model: gpt-4o) to translate
    log messages that may be visible to support teams into the target language.
    The provider is identified through the openai SDK import and the model
    identifier "gpt-4o".
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    messages_to_translate = log_messages[:max_messages]

    if not messages_to_translate and service:
        error_results = query_error_logs(
            service=service,
            time_range_minutes=time_range_minutes,
            limit=max_messages,
        )
        messages_to_translate = [log["message"] for log in error_results.logs[:max_messages]]

    translations = []

    for idx, message in enumerate(messages_to_translate):
        prompt = (
            f"Translate the following log message to {target_language}. "
            f"Keep technical terms like error codes, file paths, and identifiers in English. "
            f"Return only the translation, nothing else.\n\n"
            f"Log message: {message}"
        )

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a professional technical translator. Translate log messages to {target_language} for support teams. Keep technical identifiers, error codes, paths, and URLs in English.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=256,
        )

        translated_text = response.choices[0].message.content.strip()
        translations.append({
            "index": idx,
            "original": message,
            "translated": translated_text,
            "target_language": target_language,
        })

    return translations


def format_translations(translations: list[dict]) -> str:
    """Format translation results for display."""
    lines = ["=== Log Message Translations ===", ""]
    for t in translations:
        lines.append(f"Original ({t.get('source_language', 'en')}): {t['original']}")
        lines.append(f"Translated ({t['target_language']}): {t['translated']}")
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    sample_messages = [
        "Database connection timeout after 30 seconds",
        "Failed to authenticate user: invalid credentials",
        "SSL certificate verification failed for api.example.com",
        "Rate limit exceeded: 100 requests per minute",
    ]
    results = translate_log_messages(
        sample_messages,
        target_language="Spanish",
    )
    print(format_translations(results))
