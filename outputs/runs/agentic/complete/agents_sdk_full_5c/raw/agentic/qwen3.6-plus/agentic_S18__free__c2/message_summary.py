"""Summarize message processing results using OpenAI GPT-4o.

Takes message processing results and generates a summary of
processing performance, error patterns, and key insights.
"""

import json
from typing import List, Dict, Any

from openai import OpenAI

from messaging_models import MessageProcessingResult, ConsumedMessage


_OPENAI_MODEL_ID = "gpt-4o"


def summarize_processing_results(
    results: List[MessageProcessingResult],
    max_summary_length: int = 500,
) -> str:
    """Summarize message processing results using OpenAI GPT-4o.

    Args:
        results: List of MessageProcessingResult objects.
        max_summary_length: Maximum length of the summary.

    Returns:
        Human-readable summary of processing results.
    """
    result_data = [
        {
            "message_id": r.message_id,
            "event_type": r.event_type,
            "status": r.status,
            "processing_time_ms": r.processing_time_ms,
            "error_message": r.error_message,
            "processed_at": r.processed_at,
        }
        for r in results
    ]

    prompt = (
        f"Summarize the following message processing results. "
        f"Include key metrics like success rate, average processing time, "
        f"common error patterns, and event type distribution. "
        f"Keep the summary under {max_summary_length} characters.\n\n"
        f"Processing Results:\n{json.dumps(result_data, indent=2)}"
    )

    client = OpenAI()
    response = client.chat.completions.create(
        model=_OPENAI_MODEL_ID,
        messages=[
            {
                "role": "system",
                "content": "You are a message processing analyst. Provide concise summaries of Pub/Sub message processing results.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=500,
        temperature=0.3,
    )

    summary = response.choices[0].message.content.strip()
    return summary


def summarize_consumed_messages(
    messages: List[ConsumedMessage],
    focus_area: str = "general",
) -> str:
    """Summarize a batch of consumed messages using OpenAI GPT-4o.

    Args:
        messages: List of ConsumedMessage objects.
        focus_area: Focus area for summary (e.g., 'errors', 'content', 'general').

    Returns:
        Summary of the consumed messages.
    """
    message_data = [
        {
            "message_id": m.message_id,
            "event_type": m.event_type,
            "event_id": m.event_id,
            "payload": m.payload if isinstance(m.payload, dict) else str(m.payload)[:200],
            "publish_time": m.publish_time,
        }
        for m in messages
    ]

    prompt = (
        f"Summarize the following consumed Pub/Sub messages. "
        f"Focus on: {focus_area}.\n\n"
        f"Messages:\n{json.dumps(message_data, indent=2, default=str)}"
    )

    client = OpenAI()
    response = client.chat.completions.create(
        model=_OPENAI_MODEL_ID,
        messages=[
            {
                "role": "system",
                "content": "You are a messaging analyst summarizing Pub/Sub message payloads and patterns.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=400,
        temperature=0.2,
    )

    return response.choices[0].message.content.strip()


def generate_processing_report(
    results: List[MessageProcessingResult],
    report_type: str = "daily",
) -> Dict[str, Any]:
    """Generate a detailed processing report using OpenAI GPT-4o.

    Args:
        results: List of processing results.
        report_type: Type of report (daily, hourly, on-demand).

    Returns:
        Dictionary with report sections.
    """
    summary = summarize_processing_results(results)

    total = len(results)
    successful = sum(1 for r in results if r.status == "success")
    failed = sum(1 for r in results if r.status == "failed")
    avg_time = (
        sum(r.processing_time_ms for r in results) / total if total > 0 else 0
    )

    return {
        "report_type": report_type,
        "total_messages": total,
        "successful": successful,
        "failed": failed,
        "success_rate": successful / total if total > 0 else 0.0,
        "avg_processing_time_ms": round(avg_time, 2),
        "summary": summary,
    }
