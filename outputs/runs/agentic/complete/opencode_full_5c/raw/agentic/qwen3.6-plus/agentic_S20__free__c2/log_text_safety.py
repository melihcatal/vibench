import os
from typing import Optional

import openai

from observability_models import LogEntry
from fetch_recent_logs import fetch_recent_logs

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = "gpt-4o"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"

openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)


def check_log_text_safety(
    text: str,
    model: str = OPENAI_MODERATION_MODEL,
) -> dict:
    result = openai_client.moderations.create(
        input=text,
        model=model,
    )
    flagged = result.results[0].flagged
    categories = result.results[0].categories.model_dump()
    category_scores = result.results[0].category_scores.model_dump()
    return {
        "flagged": flagged,
        "categories": categories,
        "category_scores": category_scores,
        "text_length": len(text),
    }


def scan_logs_for_safety(
    service: str = "",
    hours: int = 1,
    limit: int = 50,
) -> list[dict]:
    query_result = fetch_recent_logs(service=service, hours=hours, limit=limit)
    results: list[dict] = []
    for entry in query_result.entries:
        safety = check_log_text_safety(entry.message)
        results.append(
            {
                "log_id": entry.id,
                "timestamp": entry.timestamp.isoformat(),
                "service": entry.service,
                "message_preview": entry.message[:200],
                "safety": safety,
            }
        )
    return results


if __name__ == "__main__":
    sample_text = "This is a normal log message with no unsafe content."
    result = check_log_text_safety(sample_text)
    print(result)
