import os
import json
from typing import Optional

import openai

from observability_models import LogEntry
from query_error_logs import query_error_logs

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = "gpt-4o"

openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)


def build_incident_prompt(error_logs: list[LogEntry]) -> str:
    log_lines = []
    for entry in error_logs:
        attrs = json.dumps(entry.attributes) if entry.attributes else ""
        line = (
            f"- [{entry.timestamp.isoformat()}] [{entry.status}] "
            f"service={entry.service} source={entry.source} "
            f"message={entry.message}"
        )
        if attrs:
            line += f" attributes={attrs}"
        log_lines.append(line)
    logs_text = "\n".join(log_lines)
    return (
        f"You are an incident reviewer. Analyze the following error logs "
        f"and produce a concise incident summary.\n\n"
        f"Error logs:\n{logs_text}\n\n"
        f"Provide:\n"
        f"1. A brief summary of the incident\n"
        f"2. Affected services and components\n"
        f"3. Root cause hypothesis\n"
        f"4. Recommended next steps\n"
        f"5. Severity assessment"
    )


def summarize_incident(
    service: str = "",
    hours: int = 2,
    limit: int = 50,
    model: str = OPENAI_MODEL,
) -> str:
    query_result = query_error_logs(service=service, hours=hours, limit=limit)
    if not query_result.entries:
        return "No error logs found in the specified time range."

    prompt = build_incident_prompt(query_result.entries)
    response = openai_client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are an expert SRE incident analyst."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        max_tokens=1500,
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    summary = summarize_incident(service="payment-service", hours=2)
    print(summary)
