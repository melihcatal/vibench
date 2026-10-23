"""Summarize error-log findings for incident review using OpenAI GPT-4."""

import os
from datetime import datetime, timezone

from openai import OpenAI

from query_error_logs import query_error_logs
from observability_models import LogQueryResponse


def summarize_incident(
    service: str | None = None,
    time_range_minutes: int = 60,
    max_logs: int = 30,
) -> str:
    """
    Summarize recent error log findings for incident review.

    Uses the OpenAI GPT-4 model (openai package, model: gpt-4o) to generate
    a structured incident summary from Datadog error logs. The provider is
    identified through the openai SDK import and the model identifier "gpt-4o".
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    error_results = query_error_logs(
        service=service,
        time_range_minutes=time_range_minutes,
        limit=max_logs,
    )

    if not error_results.logs:
        return "No error logs found in the specified time range."

    log_context = []
    for log in error_results.logs[:max_logs]:
        log_context.append(
            f"[{log['timestamp']}] status={log['status']} service={log['service']} "
            f"host={log['hostname']} message={log['message']}"
        )

    log_text = "\n".join(log_context)

    prompt = (
        f"You are an incident response engineer. Review the following error log entries "
        f"and produce a structured incident summary.\n\n"
        f"Time range: last {time_range_minutes} minutes\n"
        f"Service: {service or 'all services'}\n"
        f"Total errors found: {error_results.total_count}\n\n"
        f"Error log entries:\n{log_text}\n\n"
        f"Provide a summary with:\n"
        f"1. Incident title\n"
        f"2. Severity assessment\n"
        f"3. Root cause analysis\n"
        f"4. Affected components\n"
        f"5. Recommended actions\n"
        f"6. Timeline of events"
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are an expert incident response engineer. Analyze error logs and produce clear, actionable incident summaries.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=2000,
    )

    summary = response.choices[0].message.content
    return summary


if __name__ == "__main__":
    summary = summarize_incident(
        service="payment-service",
        time_range_minutes=60,
        max_logs=20,
    )
    print(summary)
