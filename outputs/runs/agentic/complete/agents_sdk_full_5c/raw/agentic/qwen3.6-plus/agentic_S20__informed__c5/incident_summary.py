"""Summarize error-log findings for incident review using OpenAI GPT chat completions."""

import json
import os
from typing import Optional

from openai import OpenAI

from query_error_logs import query_error_logs


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")


def summarize_incident(
    service: str,
    environment: str = "production",
    minutes_ago: int = 60,
    max_logs: int = 50,
) -> str:
    """Fetch recent error logs and generate an incident summary using OpenAI GPT-4o.

    Uses the OpenAI chat completions API with model gpt-4o to produce
    a concise incident review summary from error log data.
    """
    error_logs = query_error_logs(
        service=service,
        environment=environment,
        minutes_ago=minutes_ago,
        limit=max_logs,
    )

    if not error_logs:
        return f"No error logs found for service '{service}' in the last {minutes_ago} minutes."

    log_lines = []
    for log in error_logs:
        log_lines.append(
            f"[{log.get('timestamp', '')}] [{log.get('status', 'UNKNOWN')}] "
            f"{log.get('message', '')} service={log.get('service', '')} "
            f"host={log.get('host', '')}"
        )

    log_context = "\n".join(log_lines)

    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an incident response analyst. "
                    "Review the provided error logs and produce a concise incident summary. "
                    "Include: root cause hypothesis, affected services, severity assessment, "
                    "and recommended next steps. Keep it under 300 words."
                ),
            },
            {
                "role": "user",
                "content": f"Error logs for service '{service}':\n\n{log_context}",
            },
        ],
        temperature=0.3,
        max_tokens=600,
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    summary = summarize_incident(
        service="payment-api",
        environment="production",
        minutes_ago=30,
    )
    print(summary)
