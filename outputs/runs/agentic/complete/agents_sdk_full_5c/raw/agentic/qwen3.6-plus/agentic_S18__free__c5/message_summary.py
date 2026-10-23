"""Summarize message processing results using OpenAI API.

Uses the openai SDK with the gpt-4o-mini model to generate concise summaries
of message processing outcomes, event payloads, and batch results.
"""

import json
import os
from typing import Any

import openai

from messaging_models import ConsumeResult, PublishResult, DeadLetterRecord


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = "gpt-4o-mini"


def _get_openai_client() -> openai.OpenAI:
    """Create and return an OpenAI API client.

    Returns:
        Configured openai.OpenAI client instance using the gpt-4o-mini model.
    """
    return openai.OpenAI(api_key=OPENAI_API_KEY)


def summarize_processing_result(
    result: ConsumeResult | PublishResult | DeadLetterRecord | dict[str, Any],
    include_details: bool = True,
    max_tokens: int = 256,
) -> str:
    """Generate a human-readable summary of a message processing result.

    Uses OpenAI's gpt-4o-mini model to create concise summaries of
    Pub/Sub message processing outcomes.

    Args:
        result: A ConsumeResult, PublishResult, DeadLetterRecord, or dict.
        include_details: Whether to include payload details in the summary.
        max_tokens: Maximum tokens for the generated summary.

    Returns:
        Generated summary string.

    Raises:
        openai.APIError: If the OpenAI API call fails.
    """
    client = _get_openai_client()

    if isinstance(result, ConsumeResult):
        result_type = "message_consumption"
        data = {
            "event_id": result.event.event_id,
            "event_type": result.event.event_type,
            "source": result.event.source,
            "delivery_attempt": result.delivery_attempt,
            "payload": result.event.payload if include_details else None,
        }
    elif isinstance(result, PublishResult):
        result_type = "message_publish"
        data = {
            "topic": result.topic,
            "count": result.count,
            "message_ids": result.message_ids,
        }
    elif isinstance(result, DeadLetterRecord):
        result_type = "dead_letter"
        data = {
            "original_event_id": result.original_event_id,
            "failure_reason": result.failure_reason,
            "retry_count": result.retry_count,
            "dead_letter_message_id": result.dead_letter_message_id,
        }
    else:
        result_type = "custom"
        data = result

    prompt = (
        f"Summarize this {result_type} result for a messaging system operator report. "
        f"Keep it concise (2-3 sentences). Focus on what happened and any actionable items.\n\n"
        f"Data: {json.dumps(data, default=str)}"
    )

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a messaging system analyst. Summarize processing results "
                    "clearly and concisely for operations teams."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=max_tokens,
        temperature=0.3,
    )

    return response.choices[0].message.content.strip()


def summarize_batch_results(
    results: list[dict[str, Any]],
    max_tokens: int = 512,
) -> str:
    """Generate a summary of multiple processing results using gpt-4o-mini.

    Args:
        results: List of processing result dictionaries.
        max_tokens: Maximum tokens for the generated summary.

    Returns:
        Generated batch summary string.
    """
    client = _get_openai_client()

    prompt = (
        f"Summarize these {len(results)} messaging processing results. "
        f"Group by event type, note any failures or dead-lettered messages, "
        f"and provide an overall health assessment.\n\n"
        f"Results: {json.dumps(results, default=str)}"
    )

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a messaging system analyst. Provide batch processing "
                    "summaries that highlight patterns, issues, and overall system health."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=max_tokens,
        temperature=0.3,
    )

    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    sample_result = {
        "event_id": "evt-123",
        "event_type": "order.created",
        "status": "processed",
        "duration_ms": 45,
    }
    summary = summarize_processing_result(sample_result)
    print(f"Summary: {summary}")
