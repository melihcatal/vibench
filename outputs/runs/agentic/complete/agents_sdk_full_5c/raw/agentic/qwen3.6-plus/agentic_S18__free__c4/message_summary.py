"""Summarize message processing results using OpenAI API.

Uses the openai SDK to generate natural language summaries of message
processing outcomes, including success rates, error patterns, and trends.
"""

import os
import json
from typing import Optional, Dict, Any, List

from openai import OpenAI

# OpenAI model identifier for summarization
SUMMARY_MODEL = "gpt-4o-mini"


def summarize_processing_results(
    processing_results: List[Dict[str, Any]],
    model: str = SUMMARY_MODEL,
    include_recommendations: bool = True,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """Generate a summary of message processing results using OpenAI.

    Args:
        processing_results: List of ProcessingResult dicts with status,
            error_message, event_type, etc.
        model: OpenAI model identifier to use.
        include_recommendations: Whether to include improvement suggestions.
        api_key: OpenAI API key. Falls back to OPENAI_API_KEY env var.

    Returns:
        Dict with summary text and structured analysis.
    """
    if api_key is None:
        api_key = os.environ.get("OPENAI_API_KEY")

    client = OpenAI(api_key=api_key)

    total = len(processing_results)
    success_count = sum(1 for r in processing_results if r.get("status") == "success")
    failed_count = sum(1 for r in processing_results if r.get("status") == "failed")
    dlq_count = sum(1 for r in processing_results if r.get("status") == "dead_lettered")

    error_messages = [
        r.get("error_message", "") for r in processing_results
        if r.get("status") in ("failed", "dead_lettered") and r.get("error_message")
    ]

    event_types = {}
    for r in processing_results:
        et = r.get("event_type", "unknown")
        if et not in event_types:
            event_types[et] = {"total": 0, "success": 0, "failed": 0}
        event_types[et]["total"] += 1
        if r.get("status") == "success":
            event_types[et]["success"] += 1
        elif r.get("status") in ("failed", "dead_lettered"):
            event_types[et]["failed"] += 1

    stats = {
        "total_processed": total,
        "success_count": success_count,
        "failed_count": failed_count,
        "dead_lettered_count": dlq_count,
        "success_rate": round(success_count / total * 100, 2) if total > 0 else 0,
        "event_type_breakdown": event_types,
        "top_errors": error_messages[:10],
    }

    prompt = (
        f"Summarize the following message processing results:\n\n"
        f"Total messages: {total}\n"
        f"Successful: {success_count}\n"
        f"Failed: {failed_count}\n"
        f"Dead-lettered: {dlq_count}\n"
        f"Success rate: {stats['success_rate']}%\n\n"
        f"Event type breakdown:\n{json.dumps(event_types, indent=2)}\n\n"
        f"Sample errors:\n{json.dumps(error_messages[:5], indent=2)}\n\n"
        f"Provide a concise summary of the processing results, highlight any "
        f"notable patterns or issues, and include actionable recommendations "
        f"{'for improving reliability.' if include_recommendations else 'for system health.'}"
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a messaging system analyst. Provide clear, concise summaries of message processing results with data-driven insights."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=500,
    )

    summary_text = response.choices[0].message.content

    return {
        "status": "summarized",
        "model_used": model,
        "statistics": stats,
        "summary": summary_text,
        "input_message_count": total,
    }


def summarize_single_message(
    message_data: Dict[str, Any],
    processing_result: Dict[str, Any],
    model: str = SUMMARY_MODEL,
) -> Dict[str, Any]:
    """Summarize a single message processing outcome.

    Args:
        message_data: Original message payload and metadata.
        processing_result: Result of processing the message.
        model: OpenAI model to use.

    Returns:
        Dict with summary of the single message outcome.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)

    prompt = (
        f"Summarize this message processing outcome in one sentence:\n"
        f"Message: {json.dumps(message_data, indent=2)}\n"
        f"Result: {json.dumps(processing_result, indent=2)}"
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Provide a one-sentence summary of message processing results."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=100,
        temperature=0.2,
    )

    return {
        "status": "summarized",
        "model_used": model,
        "summary": response.choices[0].message.content,
        "message_id": message_data.get("event_id", "unknown"),
        "processing_status": processing_result.get("status", "unknown"),
    }


if __name__ == "__main__":
    sample_results = [
        {"event_id": "evt-1", "event_type": "order.created", "status": "success"},
        {"event_id": "evt-2", "event_type": "order.created", "status": "success"},
        {"event_id": "evt-3", "event_type": "payment.failed", "status": "failed", "error_message": "Invalid card"},
        {"event_id": "evt-4", "event_type": "order.created", "status": "dead_lettered", "error_message": "Schema mismatch"},
    ]

    result = summarize_processing_results(sample_results)
    print(json.dumps(result, indent=2))
