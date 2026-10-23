"""
[LATER-STEP] Checks selected log message text for unsafe content.

Uses the OpenAI Moderation API (api.openai.com) to scan log messages for
potentially unsafe, sensitive, or policy-violating content before sharing
in support-visible channels.
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any, Dict, List, Optional

import openai
from openai import OpenAI


def get_openai_client() -> OpenAI:
    """
    Create an OpenAI client configured from environment variables.

    Requires OPENAI_API_KEY environment variable.
    """
    api_key = os.environ.get("OPENAI_API_KEY", "")
    client = OpenAI(api_key=api_key)
    return client


def check_log_safety(
    log_message: str,
    client: Optional[OpenAI] = None,
) -> Dict[str, Any]:
    """
    Check a single log message for unsafe content using OpenAI Moderation API.

    Sends the log text to the OpenAI moderation endpoint and returns
    category scores and a flagged status.

    Args:
        log_message: The log message text to check.
        client: Optional pre-configured OpenAI client.

    Returns:
        Dictionary with flagged status, category scores, and the original text.
    """
    if client is None:
        client = get_openai_client()

    response = client.moderations.create(
        model="omni-moderation-latest",
        input=log_message,
    )

    result = response.results[0]
    return {
        "flagged": result.flagged,
        "categories": dict(result.categories),
        "category_scores": dict(
            (k, round(v, 4)) for k, v in result.category_scores.items()
        ),
        "text": log_message,
    }


def check_multiple_log_messages(
    messages: List[str],
    client: Optional[OpenAI] = None,
    batch_size: int = 10,
) -> List[Dict[str, Any]]:
    """
    Check multiple log messages for unsafe content.

    Processes messages in batches respecting the OpenAI API limits.

    Args:
        messages: List of log messages to check.
        client: Optional pre-configured OpenAI client.
        batch_size: Number of messages per moderation call.

    Returns:
        List of safety check results for each message.
    """
    if client is None:
        client = get_openai_client()

    all_results = []
    for i in range(0, len(messages), batch_size):
        batch = messages[i : i + batch_size]
        response = client.moderations.create(
            model="omni-moderation-latest",
            input=batch,
        )
        for j, result in enumerate(response.results):
            all_results.append(
                {
                    "flagged": result.flagged,
                    "categories": dict(result.categories),
                    "category_scores": dict(
                        (k, round(v, 4)) for k, v in result.category_scores.items()
                    ),
                    "text": batch[j],
                }
            )
    return all_results


def filter_unsafe_logs(
    log_messages: List[str],
    client: Optional[OpenAI] = None,
) -> Dict[str, Any]:
    """
    Separate log messages into safe and unsafe categories.

    Args:
        log_messages: List of log messages to filter.
        client: Optional pre-configured OpenAI client.

    Returns:
        Dictionary with lists of safe and unsafe messages plus counts.
    """
    results = check_multiple_log_messages(log_messages, client=client)

    safe_messages = [r["text"] for r in results if not r["flagged"]]
    unsafe_messages = [r for r in results if r["flagged"]]

    return {
        "safe_count": len(safe_messages),
        "unsafe_count": len(unsafe_messages),
        "safe_messages": safe_messages,
        "unsafe_results": unsafe_messages,
        "total_checked": len(results),
    }


def main() -> None:
    """Example: check log messages for unsafe content."""
    test_logs = [
        "User login successful for user@example.com",
        "Payment processed: $50.00 charged to card ending 4242",
        "ERROR: Unhandled exception in /api/data processing",
        "This message contains nothing problematic.",
    ]

    result = filter_unsafe_logs(test_logs)
    print(json.dumps(result, indent=2))

    if result["unsafe_count"] > 0:
        print(f"\n⚠️  {result['unsafe_count']} message(s) flagged for review", file=sys.stderr)


if __name__ == "__main__":
    main()
