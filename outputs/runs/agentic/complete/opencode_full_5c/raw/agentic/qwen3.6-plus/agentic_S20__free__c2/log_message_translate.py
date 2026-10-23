import os
from typing import Optional

import openai

from observability_models import LogEntry
from fetch_recent_logs import fetch_recent_logs

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = "gpt-4o"

openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)


def translate_log_message(
    text: str,
    target_locale: str = "es",
    model: str = OPENAI_MODEL,
) -> str:
    locale_names = {
        "es": "Spanish",
        "fr": "French",
        "de": "German",
        "ja": "Japanese",
        "zh": "Chinese",
        "pt": "Portuguese",
        "ko": "Korean",
        "it": "Italian",
    }
    target_name = locale_names.get(target_locale, target_locale)
    response = openai_client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    f"You are a professional translator. Translate the following "
                    f"log message into {target_name}. Preserve any technical terms, "
                    "IDs, codes, and structured data exactly as they appear. "
                    "Return only the translated text."
                ),
            },
            {"role": "user", "content": text},
        ],
        temperature=0.1,
        max_tokens=500,
    )
    return response.choices[0].message.content.strip()


def translate_recent_logs(
    service: str = "",
    target_locale: str = "es",
    hours: int = 1,
    limit: int = 20,
) -> list[dict]:
    query_result = fetch_recent_logs(service=service, hours=hours, limit=limit)
    results: list[dict] = []
    for entry in query_result.entries:
        translated = translate_log_message(entry.message, target_locale)
        results.append(
            {
                "log_id": entry.id,
                "timestamp": entry.timestamp.isoformat(),
                "service": entry.service,
                "original": entry.message,
                "translated": translated,
                "target_locale": target_locale,
            }
        )
    return results


if __name__ == "__main__":
    result = translate_log_message(
        "Database connection timeout after 30s retry limit exceeded",
        target_locale="es",
    )
    print(result)
