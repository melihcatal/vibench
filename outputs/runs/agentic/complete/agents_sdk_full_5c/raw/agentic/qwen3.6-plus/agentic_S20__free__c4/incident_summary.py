"""
Summarize error-log findings for incident review.

Uses the Datadog Logs API (api.datadoghq.com) via the datadog-api-client SDK
to retrieve recent error logs, then uses OpenAI's GPT-4 model
(api.openai.com) via the openai Python SDK to generate an incident
summary from the collected error log data.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional

import openai
from openai import OpenAI

from observability_models import (
    LogQueryFilter,
    LogEntry,
    QueryResult,
    LogLevel,
    build_error_query,
)
from observability_client import query_logs

OPENAI_API_HOST = "https://api.openai.com/v1"


def summarize_incident_errors(
    severity: str = "error",
    service: Optional[str] = None,
    time_window_minutes: int = 60,
    openai_model: str = "gpt-4o",
    max_summary_tokens: int = 1024,
) -> Dict[str, Any]:
    """Summarize error logs for incident review using OpenAI GPT-4.

    First retrieves recent error logs from Datadog's managed logging service
    at api.datadoghq.com using the datadog-api-client SDK, then sends the
    error data to OpenAI's GPT-4 model (gpt-4o) via api.openai.com to
    generate a structured incident summary.

    Args:
        severity: Log severity level to query.
        service: Optional service name filter.
        time_window_minutes: Time window for error log retrieval.
        openai_model: OpenAI model to use for summarization (e.g., gpt-4o, gpt-4-turbo).
        max_summary_tokens: Maximum tokens for the generated summary.

    Returns:
        Dict with incident summary, raw error data, and metadata.
    """
    filter_query = build_error_query(
        severity=LogLevel(severity.lower()),
        service=service,
        time_window_minutes=time_window_minutes,
    )
    filter_query.limit = 100

    log_result: QueryResult = query_logs(filter_query)

    error_entries = []
    for entry in log_result.entries:
        error_entries.append({
            "timestamp": entry.timestamp,
            "message": entry.message,
            "service": entry.service,
            "status": entry.status,
            "correlation_id": entry.correlation_id,
            "attributes": entry.attributes,
        })

    if not error_entries:
        return {
            "summary": "No error logs found in the specified time window.",
            "error_count": 0,
            "time_window_minutes": time_window_minutes,
            "severity_filter": severity,
            "entries": [],
        }

    error_context = _build_error_context(error_entries)

    openai_client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY", ""),
        base_url=OPENAI_API_HOST,
    )

    system_prompt = (
        "You are an incident response analyst. Analyze the provided error log "
        "entries and generate a structured incident summary. Include: "
        "1) A brief executive summary of the incident. "
        "2) Root cause indicators from the logs. "
        "3) Affected services and components. "
        "4) Timeline of key error events. "
        "5) Recommended next steps for investigation. "
        "Format as JSON with keys: executive_summary, root_cause_indicators, "
        "affected_services, timeline, recommendations."
    )

    user_prompt = (
        f"Analyze these {len(error_entries)} error log entries collected from "
        f"Datadog logs over the past {time_window_minutes} minutes:\n\n"
        f"{error_context}\n\n"
        f"Generate a structured incident summary."
    )

    response = openai_client.chat.completions.create(
        model=openai_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=max_summary_tokens,
        temperature=0.3,
        response_format={"type": "json_object"},
    )

    summary_text = response.choices[0].message.content or ""
    try:
        summary_data = json.loads(summary_text)
    except json.JSONDecodeError:
        summary_data = {"raw_summary": summary_text}

    return {
        "summary": summary_data,
        "model_used": openai_model,
        "provider": "openai",
        "error_count": log_result.total_count,
        "analyzed_entries": len(error_entries),
        "time_window_minutes": time_window_minutes,
        "severity_filter": severity,
        "service_filter": service,
        "query": log_result.query_string,
    }


def _build_error_context(entries: List[Dict[str, Any]]) -> str:
    """Build a text context string from error log entries for the LLM."""
    lines = []
    for i, entry in enumerate(entries):
        ts = entry.get("timestamp", "unknown")
        msg = entry.get("message", "")
        svc = entry.get("service", "unknown")
        status = entry.get("status", "unknown")
        corr = entry.get("correlation_id", "")
        lines.append(
            f"[{i+1}] {ts} | {status.upper()} | {svc} | corr:{corr}\n"
            f"    {msg}"
        )
    return "\n".join(lines)


def main() -> None:
    """CLI entry point for generating an incident summary."""
    severity = os.environ.get("LOG_SEVERITY", "error")
    service = os.environ.get("LOG_SERVICE", None) or None
    time_window = int(os.environ.get("LOG_TIME_WINDOW", "60"))
    model = os.environ.get("OPENAI_MODEL", "gpt-4o")

    result = summarize_incident_errors(
        severity=severity,
        service=service,
        time_window_minutes=time_window,
        openai_model=model,
    )
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
