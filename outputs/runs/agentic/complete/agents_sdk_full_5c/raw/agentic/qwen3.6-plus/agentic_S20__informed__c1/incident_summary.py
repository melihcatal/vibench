"""Summarize error-log findings for incident review using OpenAI GPT."""

import json
import os
from typing import List, Optional

import openai
from openai import OpenAI

from observability_models import LogEntry, LogQueryResponse


def summarize_incident(
    log_entries: List[LogEntry],
    incident_title: str,
    model: str = "gpt-4o",
    api_key: Optional[str] = None,
) -> dict:
    """Summarize error-log findings for incident review using OpenAI Chat Completions.

    Uses the OpenAI SDK (openai) with OPENAI_API_KEY for authentication
    against the OpenAI GPT service. The concrete model family is GPT-4o
    (gpt-4o).
    """
    client = OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY"))

    log_context = ""
    for i, entry in enumerate(log_entries[:50], 1):
        log_context += (
            f"[{i}] {entry.timestamp.isoformat()} | {entry.severity} | "
            f"{entry.message}\n"
            f"    Labels: {json.dumps(entry.labels)}\n"
        )

    system_prompt = (
        "You are an incident response analyst. Summarize the error-log findings "
        "provided by the user into a concise incident review report. Include:\n"
        "1. A brief overview of the incident\n"
        "2. Key errors identified with timestamps\n"
        "3. Affected services or components\n"
        "4. Recommended next steps for investigation\n"
        "Keep the summary professional and actionable."
    )

    user_prompt = (
        f"Incident: {incident_title}\n\n"
        f"Error log entries ({len(log_entries)} total):\n\n"
        f"{log_context}"
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
        max_tokens=1500,
    )

    summary_text = response.choices[0].message.content

    return {
        "incident_title": incident_title,
        "model": model,
        "provider": "OpenAI GPT",
        "log_entries_analyzed": len(log_entries),
        "summary": summary_text,
        "usage": {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens,
        }
    }


def main():
    from datetime import datetime, timezone

    sample_entries = [
        LogEntry(
            timestamp=datetime(2025, 1, 15, 10, 23, 0, tzinfo=timezone.utc),
            severity="ERROR",
            message="Database connection pool exhausted: max connections reached",
            labels={"service": "db-proxy", "region": "us-east-1"},
        ),
        LogEntry(
            timestamp=datetime(2025, 1, 15, 10, 23, 15, tzinfo=timezone.utc),
            severity="ERROR",
            message="Request timeout after 30s: POST /api/checkout",
            labels={"service": "order-service", "correlation_id": "abc-123"},
        ),
        LogEntry(
            timestamp=datetime(2025, 1, 15, 10, 24, 0, tzinfo=timezone.utc),
            severity="CRITICAL",
            message="Circuit breaker tripped for payment-gateway service",
            labels={"service": "payment-service", "circuit": "payment-gateway"},
        ),
    ]

    result = summarize_incident(
        log_entries=sample_entries,
        incident_title="Checkout service degradation - 2025-01-15",
        model="gpt-4o",
    )
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
