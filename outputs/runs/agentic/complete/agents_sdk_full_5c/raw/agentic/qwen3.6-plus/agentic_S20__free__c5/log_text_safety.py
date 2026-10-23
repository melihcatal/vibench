"""Check selected log message text for unsafe content using OpenAI Moderation API.

Provider (log query): Datadog Logs API v2
- Endpoint: POST https://api.datadoghq.com/api/v2/logs/events/search
- SDK: datadog-api-client (datadog_api_client.v2.api.logs_api.LogsApi)

Provider (safety check): OpenAI Moderation API
- Model: omni-moderation-latest
- Endpoint: https://api.openai.com/v1/moderations
- SDK: openai
"""

import os
import json
from typing import Optional

from openai import OpenAI
from fetch_recent_logs import fetch_recent_logs
from observability_models import LogQueryResponse
from observability_client import DatadogObservabilityClient


OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def check_log_safety(
    service: str,
    hours: int = 1,
    limit: int = 50,
    client: Optional[DatadogObservabilityClient] = None,
    openai_client: Optional[OpenAI] = None,
) -> dict:
    """Fetch recent logs from Datadog and check message text for unsafe content.

    Steps:
    1. Fetch recent logs from Datadog Logs API v2 for the given service.
    2. Extract log message text.
    3. Submit each message to the OpenAI Moderation API (omni-moderation-latest)
       to detect unsafe content (hate, self-harm, sexual, violence, etc.).
    4. Return results with safety flags and category breakdowns.

    Reference: https://platform.openai.com/docs/api-reference/moderations

    Args:
        service: The service name to fetch logs for.
        hours: Number of recent hours to search.
        limit: Maximum number of log entries to check.
        client: Optional pre-configured DatadogObservabilityClient.
        openai_client: Optional pre-configured OpenAI client.

    Returns:
        Dict with per-message safety analysis and overall assessment.
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
            })

    safety_results = []
    flagged_count = 0
    for entry in messages:
        mod_result = _check_single_message(openai_client, entry["message"])
        is_flagged = mod_result.get("flagged", False)
        if is_flagged:
            flagged_count += 1
        safety_results.append({
            "timestamp": entry["timestamp"],
            "message": entry["message"],
            "flagged": is_flagged,
            "categories": mod_result.get("categories", {}),
            "category_scores": mod_result.get("category_scores", {}),
        })

    overall_safe = flagged_count == 0
    return {
        "service": service,
        "total_logs_checked": len(safety_results),
        "flagged_count": flagged_count,
        "overall_safe": overall_safe,
        "model_used": OPENAI_MODERATION_MODEL,
        "results": safety_results,
    }


def _check_single_message(openai_client: OpenAI, message: str) -> dict:
    """Check a single log message using the OpenAI Moderation API."""
    response = openai_client.moderations.create(
        model=OPENAI_MODERATION_MODEL,
        input=message,
    )

    result = response.results[0]
    categories = {}
    category_scores = {}
    if hasattr(result, "categories") and result.categories:
        for cat_name in result.categories.__dict__:
            val = getattr(result.categories, cat_name, False)
            if val is not None:
                categories[cat_name] = bool(val)
    if hasattr(result, "category_scores") and result.category_scores:
        for cat_name in result.category_scores.__dict__:
            val = getattr(result.category_scores, cat_name, 0)
            if val is not None:
                category_scores[cat_name] = float(val)

    return {
        "flagged": result.flagged,
        "categories": categories,
        "category_scores": category_scores,
    }


def main():
    """Entry point for checking log message safety."""
    service = os.environ.get("LOG_SERVICE", "web-api")
    hours = int(os.environ.get("SAFETY_CHECK_HOURS", "1"))

    result = check_log_safety(service=service, hours=hours)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
