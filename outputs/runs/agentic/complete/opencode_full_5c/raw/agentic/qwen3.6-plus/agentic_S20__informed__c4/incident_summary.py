import os

import openai

from query_error_logs import query_error_logs
from observability_models import NormalizedLogEntry


OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def format_log_entries_for_summary(entries):
    lines = []
    for entry in entries:
        if isinstance(entry, dict):
            msg = entry.get("message", "")
            status = entry.get("status", "unknown")
            service = entry.get("service", "")
            timestamp = entry.get("timestamp", "")
        elif isinstance(entry, NormalizedLogEntry):
            msg = entry.message
            status = entry.status
            service = entry.service
            timestamp = entry.timestamp
        else:
            msg = str(entry)
            status = "unknown"
            service = ""
            timestamp = ""
        lines.append(f"[{timestamp}] [{status}] service={service}: {msg}")
    return "\n".join(lines)


def generate_incident_summary(
    error_logs,
    severity="error",
    service=None,
    time_from=None,
    time_to=None,
    limit=50,
):
    if isinstance(error_logs, list) and len(error_logs) > 0:
        log_entries = error_logs
    else:
        raw_response = query_error_logs(
            severity=severity,
            service=service,
            time_from=time_from,
            time_to=time_to,
            limit=limit,
        )
        data = raw_response.get("data", [])
        log_entries = [NormalizedLogEntry.from_datadog_event(evt) for evt in data]

    formatted_logs = format_log_entries_for_summary(log_entries)

    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    system_prompt = (
        "You are an incident response analyst. "
        "Summarize the error log findings into a concise incident review. "
        "Include: root cause hypothesis, affected services, severity assessment, "
        "and recommended next actions."
    )

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": (
                    f"Summarize these error log entries for incident review:\n\n"
                    f"{formatted_logs}"
                ),
            },
        ],
        temperature=0.3,
        max_tokens=1024,
    )

    summary = response.choices[0].message.content
    return summary


def incident_summary(
    error_logs=None,
    severity="error",
    service=None,
    time_from=None,
    time_to=None,
    limit=50,
):
    return generate_incident_summary(
        error_logs=error_logs,
        severity=severity,
        service=service,
        time_from=time_from,
        time_to=time_to,
        limit=limit,
    )
