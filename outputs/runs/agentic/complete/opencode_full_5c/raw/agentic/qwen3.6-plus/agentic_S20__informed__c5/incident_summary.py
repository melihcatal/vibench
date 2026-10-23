import os
import sys
import json
from typing import Optional

from openai import OpenAI

from observability_models import LogEntry


def summarize_error_findings(
    error_entries: list[LogEntry],
    incident_id: Optional[str] = None,
    model: str = "gpt-4o",
) -> str:
    if not error_entries:
        return "No error log entries found for the specified time range."

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    log_context = ""
    for entry in error_entries[:50]:
        log_context += (
            f"- [{entry.timestamp}] severity={entry.severity} "
            f"service={entry.service} source={entry.source} "
            f"message={entry.message}\n"
        )

    incident_header = f"Incident ID: {incident_id}\n" if incident_id else ""

    system_prompt = (
        "You are an incident response analyst. Summarize error log findings "
        "into a concise incident review report. Identify the root cause hypothesis, "
        "affected services, error patterns, and recommended next steps."
    )

    user_prompt = (
        f"{incident_header}"
        f"Analyze the following error log entries and produce an incident summary:\n\n"
        f"{log_context}\n\n"
        f"Provide: 1) Summary of errors, 2) Affected services, 3) Root cause hypothesis, "
        f"4) Timeline of events, 5) Recommended actions."
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
        max_tokens=2048,
    )

    return response.choices[0].message.content


def main():
    log_file = sys.argv[1] if len(sys.argv) > 1 else ""
    incident_id = sys.argv[2] if len(sys.argv) > 2 else None

    if log_file:
        with open(log_file, "r") as f:
            data = json.load(f)
        entries = [LogEntry(**e) for e in data.get("entries", [])]
    else:
        entries = [
            LogEntry(
                id="sample-1",
                timestamp="2026-04-21T10:00:00Z",
                message="Connection pool exhausted",
                severity="error",
                service="api-gateway",
                source="python-app",
            ),
            LogEntry(
                id="sample-2",
                timestamp="2026-04-21T10:01:00Z",
                message="Database timeout after 30s",
                severity="error",
                service="order-service",
                source="python-app",
            ),
            LogEntry(
                id="sample-3",
                timestamp="2026-04-21T10:02:00Z",
                message="Retry limit exceeded for payment processing",
                severity="critical",
                service="payment-service",
                source="python-app",
            ),
        ]

    summary = summarize_error_findings(entries, incident_id=incident_id)
    print(summary)
    return 0


if __name__ == "__main__":
    sys.exit(main())
