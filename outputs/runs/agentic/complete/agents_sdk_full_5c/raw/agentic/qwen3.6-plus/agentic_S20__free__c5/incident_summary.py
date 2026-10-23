"""Summarize error-log findings for incident review using Datadog Logs and OpenAI.

Provider (log query): Datadog Logs API v2
- Endpoint: POST https://api.datadoghq.com/api/v2/logs/events/search
- SDK: datadog-api-client (datadog_api_client.v2.api.logs_api.LogsApi)

Provider (incident summary): OpenAI API
- Model: gpt-4o
- Endpoint: https://api.openai.com/v1/chat/completions
- SDK: openai
"""

import os
import json
from typing import Optional

from openai import OpenAI
from query_error_logs import query_error_logs, format_error_summary
from observability_models import LogQueryResponse
from observability_client import DatadogObservabilityClient


OPENAI_MODEL = "gpt-4o"


def summarize_incident(
    service: str,
    hours: int = 2,
    limit: int = 100,
    client: Optional[DatadogObservabilityClient] = None,
    openai_client: Optional[OpenAI] = None,
) -> dict:
    """Query error logs from Datadog and generate an incident review summary using OpenAI.

    Steps:
    1. Query Datadog Logs API v2 for recent error logs for the given service.
    2. Extract key error messages and patterns.
    3. Use OpenAI gpt-4o to generate an incident summary with root cause analysis.

    Args:
        service: The service name to analyze.
        hours: Number of recent hours to search for errors.
        limit: Maximum number of error log entries to analyze.
        client: Optional pre-configured DatadogObservabilityClient.
        openai_client: Optional pre-configured OpenAI client.

    Returns:
        Dict containing the raw error log data and the AI-generated incident summary.
    """
    if openai_client is None:
        openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))

    response: LogQueryResponse = query_error_logs(
        service=service,
        hours=hours,
        limit=limit,
        client=client,
    )

    if response.total_count == 0:
        return {
            "service": service,
            "hours_searched": hours,
            "error_count": 0,
            "summary": "No error logs found in the specified time window.",
        }

    log_messages = []
    for log in response.logs:
        log_messages.append({
            "timestamp": log.get("date", ""),
            "message": log.get("message", ""),
            "status": log.get("status", ""),
            "service": log.get("service", ""),
            "hostname": log.get("hostname", ""),
        })

    prompt = _build_incident_prompt(service, hours, response.total_count, log_messages)

    chat_response = openai_client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an incident response analyst. Review the provided error log "
                    "entries and produce a concise incident summary. Include: (1) a brief "
                    "overview, (2) likely root causes, (3) affected components, "
                    "(4) recommended remediation steps, and (5) severity assessment."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        max_tokens=1024,
    )

    summary_text = chat_response.choices[0].message.content.strip()

    return {
        "service": service,
        "hours_searched": hours,
        "error_count": response.total_count,
        "logs_analyzed": len(log_messages),
        "summary": summary_text,
        "model_used": OPENAI_MODEL,
    }


def _build_incident_prompt(service: str, hours: int, total_count: int, log_messages: list[dict]) -> str:
    """Build the incident analysis prompt for OpenAI gpt-4o."""
    lines = [
        f"Service: {service}",
        f"Time window: Last {hours} hours",
        f"Total errors found: {total_count}",
        f"Log entries provided: {len(log_messages)}",
        "",
        "Error log entries:",
        "-" * 40,
    ]
    for i, entry in enumerate(log_messages[:50], 1):
        lines.append(
            f"{i}. [{entry['timestamp']}] [{entry.get('hostname', 'unknown')}] "
            f"{entry['message']}"
        )
    lines.append("-" * 40)
    lines.append("\nPlease analyze these error logs and provide an incident summary.")
    return "\n".join(lines)


def main():
    """Entry point for generating an incident summary."""
    service = os.environ.get("LOG_SERVICE", "web-api")
    hours = int(os.environ.get("INCIDENT_HOURS", "2"))

    result = summarize_incident(service=service, hours=hours)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
