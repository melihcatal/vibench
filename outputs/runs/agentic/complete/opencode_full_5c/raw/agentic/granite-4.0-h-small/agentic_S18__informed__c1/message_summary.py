import json
from typing import Any
from messaging_models import (
    PublishRequest,
    PublishResponse,
    ConsumeRequest,
    ConsumeResponse,
)


def summarize(messages: list[dict]) -> dict:
    """Create a summary of message processing results.

    Args:
        messages: List of processed messages (each a dict that can be a ConsumeResponse).
    Returns:
        A dict with counts of successes, failures, and a brief overview.
    """
    success = sum(1 for m in messages if m.get("status") == "success")
    failure = len(messages) - success
    summary = {
        "total": len(messages),
        "success": success,
        "failure": failure,
        "details": [
            {
                "status": m["status"],
                "event_id": m.get("message_id"),
                "error": m.get("error"),
            }
            for m in messages
        ],
    }
    print(f"Message summary: {summary}")
    return summary
