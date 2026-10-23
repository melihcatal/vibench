"""Summarize message processing results using the Google Gemini API.

Uses the google-genai SDK to call the Gemini model for producing
concise summaries of message processing outcomes. Authentication
relies on GOOGLE_API_KEY.
"""

import os
from typing import List, Optional

from google import genai
from google.genai import types

from messaging_models import ConsumedMessage, MessageSummary, AuditRecord


MODEL_ID = "gemini-2.0-flash"


def summarize_processing_results(
    summary: MessageSummary,
    messages: Optional[List[ConsumedMessage]] = None,
    audit_records: Optional[List[AuditRecord]] = None,
) -> str:
    """Generate a natural-language summary of message processing using Gemini.

    Args:
        summary: MessageSummary with aggregate counters.
        messages: Optional list of consumed messages for context.
        audit_records: Optional list of AuditRecord entries.

    Returns:
        Human-readable summary text produced by gemini-2.0-flash.
    """
    api_key = os.environ.get("GOOGLE_API_KEY", "")
    client = genai.Client(api_key=api_key)

    context_parts: List[str] = []
    context_parts.append(
        f"Total received: {summary.total_received}, "
        f"Total processed: {summary.total_processed}, "
        f"Total failed: {summary.total_failed}, "
        f"Total dead-lettered: {summary.total_dead_lettered}, "
        f"Average processing time: {summary.avg_processing_time_ms:.1f}ms"
    )

    if messages:
        msg_summary = []
        for m in messages[:10]:
            msg_summary.append(
                f"- Event ID: {m.event_id}, Type: {m.event_type}, "
                f"Source: {m.source}, Status: {'acked' if m.acknowledged else 'pending'}"
            )
        context_parts.append("Recent messages:\n" + "\n".join(msg_summary))

    if audit_records:
        rec_summary = []
        for r in audit_records[:10]:
            rec_summary.append(
                f"- Record {r.record_id}: event_type={r.event_type}, "
                f"status={r.status}"
            )
        context_parts.append("Audit records:\n" + "\n".join(rec_summary))

    prompt = (
        "You are a messaging system analyst. Based on the following processing "
        "statistics and message details, produce a concise 3-4 sentence executive "
        "summary of the message processing pipeline health and any notable issues.\n\n"
        + "\n\n".join(context_parts)
    )

    response = client.models.generate_content(
        model=MODEL_ID,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.3,
            max_output_tokens=300,
        ),
    )

    return response.text.strip()


if __name__ == "__main__":
    s = MessageSummary(
        total_received=150,
        total_processed=142,
        total_failed=5,
        total_dead_lettered=3,
        processing_times_ms=[12.5, 8.3, 15.1, 10.0, 9.7],
    )
    text = summarize_processing_results(s)
    print(text)
