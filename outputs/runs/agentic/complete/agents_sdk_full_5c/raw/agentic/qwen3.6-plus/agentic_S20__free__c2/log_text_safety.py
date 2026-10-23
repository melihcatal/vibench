"""Check selected log message text for unsafe content using OpenAI GPT-4 moderation."""

import os
from typing import Optional

from openai import OpenAI

from query_error_logs import query_error_logs
from observability_models import LogQueryResponse


def check_log_safety(
    log_messages: list[str],
    service: str | None = None,
    time_range_minutes: int = 30,
    max_messages: int = 20,
) -> list[dict]:
    """
    Check log message text for unsafe content using OpenAI's moderation API.

    Uses the OpenAI Moderation API (openai package) to scan log messages
    for unsafe content categories. The provider is identified through the
    openai SDK import and model identifier "omni-moderation-latest".
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    safety_results = []
    messages_to_check = log_messages[:max_messages]

    if not messages_to_check and service:
        error_results = query_error_logs(
            service=service,
            time_range_minutes=time_range_minutes,
            limit=max_messages,
        )
        messages_to_check = [log["message"] for log in error_results.logs[:max_messages]]

    for idx, message in enumerate(messages_to_check):
        moderation = client.moderations.create(
            model="omni-moderation-latest",
            input=message,
        )

        result = moderation.results[0]
        flagged = result.flagged
        categories = {}
        category_scores = {}
        for cat in ["violence", "self-harm", "sexual", "hate", "harassment", "harassment/threatening", "sexual/minors"]:
            if hasattr(result.categories, cat):
                categories[cat] = getattr(result.categories, cat)
            if hasattr(result.category_scores, cat):
                category_scores[cat] = getattr(result.category_scores, cat)

        safety_results.append({
            "index": idx,
            "message": message,
            "flagged": flagged,
            "categories": categories,
            "category_scores": category_scores,
        })

    return safety_results


def generate_safety_report(results: list[dict]) -> str:
    """Generate a human-readable safety report from moderation results."""
    lines = ["=== Log Message Safety Report ===", ""]
    for r in results:
        status = "FLAGGED" if r["flagged"] else "CLEAN"
        lines.append(f"[{status}] Message {r['index']}: {r['message'][:100]}")
        if r["flagged"]:
            flagged_cats = [cat for cat, val in r["categories"].items() if val]
            lines.append(f"  Flagged categories: {', '.join(flagged_cats)}")
    lines.append("")
    total_flagged = sum(1 for r in results if r["flagged"])
    lines.append(f"Total checked: {len(results)}")
    lines.append(f"Flagged: {total_flagged}")
    lines.append(f"Clean: {len(results) - total_flagged}")
    return "\n".join(lines)


if __name__ == "__main__":
    test_messages = [
        "User login successful from IP 192.168.1.1",
        "Database connection pool exhausted, retrying",
        "Payment processing failed for order #12345",
        "Error: unauthorized access attempt to admin endpoint",
    ]
    results = check_log_safety(test_messages)
    report = generate_safety_report(results)
    print(report)
