"""
Summarizes error-log findings for incident review using OpenAI GPT model.
Provider: OpenAI Chat Completions API
Auth: OPENAI_API_KEY
"""

import os
import json
from typing import List
from openai import OpenAI
from observability_models import LogEntry


MODEL_ID = "gpt-4o"


def build_incident_summary_prompt(error_entries: List[LogEntry]) -> str:
    """Build a prompt for summarizing incident-related error logs."""
    log_lines = []
    for entry in error_entries:
        log_lines.append(
            f"- [{entry.status}] (ts={entry.timestamp}) {entry.message} | "
            f"service={entry.service} host={entry.hostname} "
            f"correlation_id={entry.correlation_id or 'N/A'}"
        )
    prompt = (
        "You are an incident response analyst. Review the following error logs "
        "and produce a concise incident summary.\n\n"
        "For each distinct issue observed, describe:\n"
        "1. What happened\n"
        "2. Which service/component was affected\n"
        "3. How many occurrences were seen\n"
        "4. A recommended next action\n\n"
        "End with a brief severity assessment (critical / high / medium / low).\n\n"
        "Error log entries:\n" + "\n".join(log_lines)
    )
    return prompt


def summarize_error_logs(
    error_entries: List[LogEntry],
    model: str = MODEL_ID,
) -> str:
    """Use OpenAI GPT to generate an incident summary from error log entries."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)
    prompt = build_incident_summary_prompt(error_entries)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are an expert SRE analyst."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=1024,
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    from datetime import timezone

    sample_entries = [
        LogEntry(
            message="Connection pool exhausted for primary database",
            status="error",
            timestamp=1700000000,
            service="payment-service",
            hostname="prod-db-01",
        ),
        LogEntry(
            message="Retry limit exceeded for payment gateway call",
            status="critical",
            timestamp=1700000060,
            service="payment-service",
            hostname="prod-worker-02",
            correlation_id="abc-123",
        ),
    ]
    summary = summarize_error_logs(sample_entries)
    print(summary)
