"""
Check selected log message text for unsafe content.

Uses the OpenAI Moderation API (api.openai.com) via the openai Python SDK
with the omni-moderation-latest model to analyze log messages for
potentially unsafe or policy-violating content.
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
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def check_log_text_safety(
    log_messages: List[str],
    model: str = OPENAI_MODERATION_MODEL,
) -> Dict[str, Any]:
    """Check log message text for unsafe content using OpenAI Moderation.

    Sends log messages to the OpenAI Moderation API at api.openai.com
    using the omni-moderation-latest model to detect content that may
    violate safety policies (hate, self-harm, sexual, violence, etc.).

    Args:
        log_messages: List of log message strings to evaluate.
        model: OpenAI moderation model identifier.

    Returns:
        Dict with safety assessment results per message.
    """
    openai_client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY", ""),
        base_url=OPENAI_API_HOST,
    )

    results = []
    flagged_count = 0

    for idx, message in enumerate(log_messages):
        if not message or not message.strip():
            continue

        response = openai_client.moderations.create(
            model=model,
            input=message,
        )

        mod_result = response.results[0]
        is_flagged = mod_result.flagged

        if is_flagged:
            flagged_count += 1

        categories = {}
        category_scores = {}
        for cat_name in dir(mod_result.categories):
            if not cat_name.startswith("_"):
                cat_value = getattr(mod_result.categories, cat_name, None)
                if isinstance(cat_value, bool):
                    categories[cat_name] = cat_value
        for cat_name in dir(mod_result.category_scores):
            if not cat_name.startswith("_"):
                cat_score = getattr(mod_result.category_scores, cat_name, None)
                if isinstance(cat_score, (int, float)):
                    category_scores[cat_name] = round(cat_score, 6)

        results.append({
            "index": idx,
            "message_preview": message[:200],
            "flagged": is_flagged,
            "categories": categories,
            "category_scores": category_scores,
        })

    return {
        "model": model,
        "provider": "openai",
        "provider_endpoint": OPENAI_API_HOST,
        "total_checked": len(results),
        "flagged_count": flagged_count,
        "clean_count": len(results) - flagged_count,
        "results": results,
    }


def check_recent_logs_safety(
    service: Optional[str] = None,
    time_window_minutes: int = 60,
    limit: int = 20,
    model: str = OPENAI_MODERATION_MODEL,
) -> Dict[str, Any]:
    """Fetch recent logs from Datadog and check them for unsafe content.

    First queries api.datadoghq.com via the datadog-api-client SDK
    for recent log messages, then evaluates them using the OpenAI
    Moderation API (omni-moderation-latest model).
    """
    now = datetime.now(timezone.utc)
    time_from = now - timedelta(minutes=time_window_minutes)

    filter_fields = {}
    if service:
        filter_fields["service"] = service

    filter_query = LogQueryFilter(
        query="",
        time_from=time_from,
        time_to=now,
        limit=limit,
        filter_fields=filter_fields,
    )

    log_result: QueryResult = query_logs(filter_query)

    messages = [entry.message for entry in log_result.entries if entry.message]

    safety_result = check_log_text_safety(messages, model=model)
    safety_result["source"] = "datadog"
    safety_result["log_query"] = log_result.query_string
    safety_result["total_log_entries"] = len(log_result.entries)

    return safety_result


def main() -> None:
    """CLI entry point for checking log text safety."""
    service = os.environ.get("LOG_SERVICE", None) or None
    time_window = int(os.environ.get("LOG_TIME_WINDOW", "60"))
    limit = int(os.environ.get("LOG_LIMIT", "20"))

    result = check_recent_logs_safety(
        service=service,
        time_window_minutes=time_window,
        limit=limit,
    )
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
