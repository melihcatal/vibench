import os
import json
from typing import List, Dict, Any, Optional

from openai import OpenAI

from fetch_recent_logs import fetch_recent_logs
from observability_models import LogEntry


OPENAI_MODEL = "gpt-4o"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")


def translate_log_message(
    message: str,
    target_language: str = "es",
    source_language: str = "en",
) -> Dict[str, Any]:
    client = OpenAI(api_key=OPENAI_API_KEY)

    system_prompt = (
        f"You are a technical translator specializing in software log messages. "
        f"Translate the following log message from {source_language} to {target_language}. "
        f"Preserve technical terms, variable names, error codes, and placeholders exactly as they appear. "
        f"Only return the translated text, nothing else."
    )

    completion = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message},
        ],
        temperature=0.1,
        max_tokens=500,
    )

    translated = completion.choices[0].message.content.strip()

    return {
        "original": message,
        "translated": translated,
        "source_language": source_language,
        "target_language": target_language,
        "model_used": OPENAI_MODEL,
    }


def translate_log_messages(
    messages: List[str],
    target_language: str = "es",
    source_language: str = "en",
) -> List[Dict[str, Any]]:
    results = []
    for message in messages:
        translation = translate_log_message(
            message=message,
            target_language=target_language,
            source_language=source_language,
        )
        results.append(translation)
    return results


def translate_recent_log_messages(
    service: Optional[str] = None,
    level: Optional[str] = None,
    time_from: Optional[str] = None,
    time_to: Optional[str] = None,
    limit: int = 10,
    target_language: str = "es",
    source_language: str = "en",
    field_filters: Optional[Dict[str, str]] = None,
) -> List[Dict[str, Any]]:
    response = fetch_recent_logs(
        service=service,
        level=level,
        time_from=time_from,
        time_to=time_to,
        limit=limit,
        field_filters=field_filters,
    )

    results = []
    for entry in response.entries:
        translation = translate_log_message(
            message=entry.message,
            target_language=target_language,
            source_language=source_language,
        )
        translation["log_id"] = entry.id
        translation["timestamp"] = entry.timestamp
        translation["service"] = entry.service
        results.append(translation)

    return results


if __name__ == "__main__":
    test_messages = [
        "Connection refused: unable to reach database server at db-primary:5432",
        "Request timeout after 30000ms for endpoint /api/v2/users",
        "Authentication failed for user admin@example.com",
    ]
    results = translate_log_messages(test_messages, target_language="ja")
    print(json.dumps(results, indent=2))
