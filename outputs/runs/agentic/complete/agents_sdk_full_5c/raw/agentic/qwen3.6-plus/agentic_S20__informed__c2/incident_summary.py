"""
incident_summary.py

Summarize error-log findings for incident review using the Anthropic
Messages API (Claude models) via the anthropic SDK.

Required env: ANTHROPIC_API_KEY
"""

import os
import json
from typing import List, Dict, Any
from anthropic import Anthropic

from observability_models import QueryResponse, LogQueryResult


def summarize_incident(
    error_results: QueryResponse,
    model: str = "claude-3-5-sonnet-20241022",
    max_tokens: int = 2048,
) -> str:
    """
    Use Anthropic Claude to produce an incident-review summary from
    error-log query results.

    Args:
        error_results: QueryResponse from query_error_logs().
        model: Anthropic Claude model identifier.
        max_tokens: Maximum output tokens.

    Returns:
        Markdown-formatted incident summary string.
    """
    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    log_entries = [r for r in error_results.results if r.message]
    sample = log_entries[:20]

    formatted_entries = []
    for i, entry in enumerate(sample, 1):
        formatted_entries.append(
            f"Entry {i}:\n"
            f"  timestamp: {entry.timestamp}\n"
            f"  level: {entry.level}\n"
            f"  service: {entry.raw_fields.get('service', 'N/A')}\n"
            f"  correlation_id: {entry.correlation_id or 'N/A'}\n"
            f"  message: {entry.message}\n"
        )

    body = "\n".join(formatted_entries)

    system_prompt = (
        "You are an incident-response analyst. Review the following error log "
        "entries extracted from Amazon CloudWatch Logs and produce a concise "
        "incident summary for the on-call team. Include:\n"
        "1. A brief overview of the incident.\n"
        "2. Affected services and components.\n"
        "3. Timeline of key events.\n"
        "4. Root-cause hypothesis.\n"
        "5. Recommended next steps."
    )

    user_message = (
        f"A total of {error_results.total_matches} error records were matched. "
        f"Below is a sample of the most recent entries:\n\n{body}"
    )

    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_message},
        ],
        temperature=0.2,
    )

    summary_text = "".join(
        block.text for block in response.content if hasattr(block, "text")
    )
    return summary_text


if __name__ == "__main__":
    from query_error_logs import query_error_logs

    lg = os.environ.get("CLOUDWATCH_LOG_GROUP", "/app/production")
    results = query_error_logs(
        log_group_name=lg,
        hours_back=2,
        log_level_filter="ERROR",
        limit=50,
    )
    summary = summarize_incident(results)
    print(summary)
