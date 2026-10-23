import os
import json
from typing import List, Dict, Any, Optional

from openai import OpenAI

from fetch_recent_logs import fetch_recent_logs
from observability_models import LogEntry


OPENAI_MODEL = "gpt-4o"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")


def check_log_text_safety(
    text: str,
) -> Dict[str, Any]:
    client = OpenAI(api_key=OPENAI_API_KEY)

    response = client.moderations.create(
        model="omni-moderation-latest",
        input=text,
    )

    result = response.results[0]
    flagged = result.flagged
    categories = {
        category: getattr(result.categories, category)
        for category in dir(result.categories)
        if not category.startswith("_")
        and isinstance(getattr(result.categories, category), bool)
    }
    category_scores = {
        category: getattr(result.category_scores, category)
        for category in dir(result.category_scores)
        if not category.startswith("_")
        and isinstance(getattr(result.category_scores, category), (int, float))
    }

    return {
        "flagged": flagged,
        "categories": categories,
        "category_scores": category_scores,
        "model_used": "omni-moderation-latest",
        "text_length": len(text),
    }


def check_logs_for_unsafe_content(
    service: Optional[str] = None,
    level: Optional[str] = None,
    time_from: Optional[str] = None,
    time_to: Optional[str] = None,
    limit: int = 20,
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
        safety_result = check_log_text_safety(entry.message)
        results.append(
            {
                "log_id": entry.id,
                "timestamp": entry.timestamp,
                "service": entry.service,
                "message_preview": entry.message[:200],
                "safety_check": safety_result,
            }
        )

    return results


def check_messages_for_unsafe_content(
    messages: List[str],
) -> List[Dict[str, Any]]:
    results = []
    for i, message in enumerate(messages):
        safety_result = check_log_text_safety(message)
        results.append(
            {
                "message_index": i,
                "message_preview": message[:200],
                "safety_check": safety_result,
            }
        )
    return results


if __name__ == "__main__":
    test_messages = [
        "Normal application log: user logged in successfully",
        "Error: database connection timeout after 30s",
    ]
    results = check_messages_for_unsafe_content(test_messages)
    print(json.dumps(results, indent=2))
