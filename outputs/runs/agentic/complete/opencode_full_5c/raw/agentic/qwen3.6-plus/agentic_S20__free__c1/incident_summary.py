import os
import json
from typing import List, Dict, Any, Optional

from openai import OpenAI

from query_error_logs import query_error_logs, format_error_log_entries
from observability_models import LogQueryResponse, LogEntry


OPENAI_MODEL = "gpt-4o"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")


def build_incident_context(error_entries: List[Dict[str, Any]]) -> str:
    lines = []
    lines.append("Error Log Summary for Incident Review")
    lines.append("=" * 40)
    lines.append(f"Total error entries: {len(error_entries)}")
    lines.append("")

    for i, entry in enumerate(error_entries[:20], 1):
        lines.append(f"--- Error {i} ---")
        lines.append(f"Timestamp: {entry.get('timestamp', 'N/A')}")
        lines.append(f"Service: {entry.get('service', 'N/A')}")
        lines.append(f"Hostname: {entry.get('hostname', 'N/A')}")
        lines.append(f"Status: {entry.get('status', 'N/A')}")
        lines.append(f"Message: {entry.get('message', 'N/A')}")
        lines.append("")

    return "\n".join(lines)


def summarize_error_logs(
    service: Optional[str] = None,
    severity: str = "error",
    time_from: Optional[str] = None,
    time_to: Optional[str] = None,
    limit: int = 50,
) -> Dict[str, Any]:
    response = query_error_logs(
        service=service,
        severity=severity,
        time_from=time_from,
        time_to=time_to,
        limit=limit,
    )

    error_entries = format_error_log_entries(response)
    context = build_incident_context(error_entries)

    client = OpenAI(api_key=OPENAI_API_KEY)

    system_prompt = (
        "You are an incident response analyst. Review the provided error log entries "
        "and produce a structured incident summary. Identify root cause patterns, "
        "affected services, severity assessment, and recommended next actions."
    )

    completion = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": context},
        ],
        temperature=0.2,
        max_tokens=1500,
    )

    summary_text = completion.choices[0].message.content

    return {
        "incident_summary": summary_text,
        "total_errors_analyzed": response.total_count,
        "entries_reviewed": len(error_entries),
        "model_used": OPENAI_MODEL,
    }


def summarize_log_entries_direct(
    entries: List[LogEntry],
) -> Dict[str, Any]:
    formatted = []
    for entry in entries:
        formatted.append(
            {
                "timestamp": entry.timestamp,
                "service": entry.service,
                "hostname": entry.hostname,
                "status": entry.status,
                "message": entry.message,
            }
        )

    context = build_incident_context(formatted)

    client = OpenAI(api_key=OPENAI_API_KEY)

    completion = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are an incident response analyst. Summarize the error logs.",
            },
            {"role": "user", "content": context},
        ],
        temperature=0.2,
        max_tokens=1500,
    )

    return {
        "incident_summary": completion.choices[0].message.content,
        "entries_reviewed": len(entries),
        "model_used": OPENAI_MODEL,
    }


if __name__ == "__main__":
    result = summarize_error_logs(
        service=os.getenv("DATADOG_SERVICE", "default-service"),
        limit=20,
    )
    print(json.dumps(result, indent=2))
