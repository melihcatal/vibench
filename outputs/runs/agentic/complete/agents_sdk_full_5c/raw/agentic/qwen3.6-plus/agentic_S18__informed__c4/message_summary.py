"""
Summarize message processing results using the Anthropic Messages API.

Uses the anthropic SDK to generate a concise summary of processed Pub/Sub
messages. Authenticated via ANTHROPIC_API_KEY with model claude-3-haiku-20240307.
"""

import os
import json
import anthropic
from typing import Any


ANTHROPIC_MODEL = "claude-3-haiku-20240307"
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
ANTHROPIC_MAX_TOKENS = 1024


def summarize_processing_results(
    messages: list[dict[str, Any]],
    processing_stats: dict[str, Any] | None = None,
) -> str:
    """
    Generate a human-readable summary of message processing results
    using the Anthropic Claude model via the Anthropic Messages API.

    Args:
        messages: List of processed message dictionaries, each containing at minimum
                  event_type, event_id, and status fields.
        processing_stats: Optional aggregate statistics (counts, rates, etc.).

    Returns:
        A text summary of the processing results.
    """
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    messages_context = json.dumps(messages, indent=2, default=str)
    stats_context = json.dumps(processing_stats, indent=2, default=str) if processing_stats else "No additional statistics provided."

    prompt = (
        f"You are a message-processing analyst. Summarize the following Pub/Sub message "
        f"processing results in a clear, concise report.\n\n"
        f"Processed Messages:\n{messages_context}\n\n"
        f"Processing Statistics:\n{stats_context}\n\n"
        f"Include: total count, breakdown by event type, success/failure rates, "
        f"any notable patterns or anomalies, and a brief conclusion."
    )

    response = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=ANTHROPIC_MAX_TOKENS,
        system="You are an expert at analyzing message-processing pipelines and producing executive summaries.",
        messages=[{"role": "user", "content": prompt}],
    )

    summary = ""
    for block in response.content:
        if block.type == "text":
            summary += block.text
    return summary


if __name__ == "__main__":
    sample_messages = [
        {"event_id": "e1", "event_type": "user.signup", "status": "success"},
        {"event_id": "e2", "event_type": "order.created", "status": "success"},
        {"event_id": "e3", "event_type": "payment.failed", "status": "error", "error": "timeout"},
    ]
    stats = {"total": 3, "success": 2, "error": 1, "success_rate": 0.67}
    result = summarize_processing_results(sample_messages, stats)
    print(result)
