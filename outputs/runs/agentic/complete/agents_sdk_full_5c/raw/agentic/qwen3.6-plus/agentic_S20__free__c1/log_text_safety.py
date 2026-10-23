"""
[LATER-STEP] log_text_safety.py

Checks selected log message text for unsafe content using OpenAI Moderation API.
Uses the openai Python SDK with the concrete OpenAI provider and moderation model.

Designed to review log messages before sharing them in support tickets or
incident reports to ensure no sensitive or unsafe content is exposed.
"""

import json
import sys
from typing import Dict, Any, List, Optional

from openai import OpenAI
from openai.types import ModerationCreateResponse

from observability_models import LogEntry


def check_log_text_safety(
    log_message: str,
    model: str = "omni-moderation-latest",
) -> Dict[str, Any]:
    """
    Check a log message for unsafe content using OpenAI Moderation API.

    Args:
        log_message: The log message text to evaluate.
        model: OpenAI moderation model identifier (default: omni-moderation-latest).

    Returns:
        Dict with safety assessment results including flagged categories.
    """
    try:
        client = OpenAI()

        response: ModerationCreateResponse = client.moderations.create(
            input=log_message,
            model=model,
        )

        result = response.results[0]
        categories = result.categories
        category_scores = result.category_scores

        flagged_categories = []
        for cat_name in dir(categories):
            if not cat_name.startswith("_"):
                value = getattr(categories, cat_name, None)
                if value is True:
                    flagged_categories.append(cat_name)

        return {
            "status": "checked",
            "flagged": result.flagged,
            "flagged_categories": flagged_categories,
            "category_scores": {
                "sexual": category_scores.sexual,
                "hate": category_scores.hate,
                "harassment": category_scores.harassment,
                "self-harm": category_scores.self_harm,
                "sexual/minors": category_scores.sexual_minors,
                "hate/threatening": category_scores.hate_threatening,
                "violence/graphic": category_scores.violence_graphic,
                "self-harm/intent": category_scores.self_harm_intent,
                "self-harm/instructions": category_scores.self_harm_instructions,
                "harassment/threatening": category_scores.harassment_threatening,
                "violence": category_scores.violence,
            },
            "message_preview": log_message[:120],
            "safe_for_sharing": not result.flagged,
        }

    except Exception as exc:
        return {
            "status": "error",
            "message": f"Failed to check log text safety with OpenAI: {exc}",
            "message_preview": log_message[:120],
        }


def check_log_entries_safety(
    entries: List[LogEntry],
    model: str = "omni-moderation-latest",
) -> Dict[str, Any]:
    """
    Check multiple log entries for unsafe content.

    Args:
        entries: List of LogEntry objects to evaluate.
        model: OpenAI moderation model identifier.

    Returns:
        Dict with batch safety results.
    """
    results = []
    any_flagged = False

    for entry in entries:
        safety_result = check_log_text_safety(entry.message, model=model)
        safety_result["entry_timestamp"] = entry.timestamp
        safety_result["entry_service"] = entry.service
        results.append(safety_result)
        if safety_result.get("flagged"):
            any_flagged = True

    return {
        "status": "batch_complete",
        "total_checked": len(results),
        "any_flagged": any_flagged,
        "flagged_count": sum(1 for r in results if r.get("flagged")),
        "results": results,
    }


def main() -> None:
    """CLI entry point for checking log text safety with OpenAI Moderation API."""
    if len(sys.argv) < 2:
        print("Usage: log_text_safety.py <log_message>")
        sys.exit(1)

    message = sys.argv[1]
    result = check_log_text_safety(message)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
