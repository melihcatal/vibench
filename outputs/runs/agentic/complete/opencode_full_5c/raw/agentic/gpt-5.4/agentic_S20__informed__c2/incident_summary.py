from __future__ import annotations

from openai import OpenAI

from observability_models import LogQueryResult


def summarize_incident(logs: list[LogQueryResult], model: str = "gpt-4.1-mini") -> str:
    client = OpenAI()
    bullet_lines = [
        f"- [{log.timestamp}] {log.severity} {log.service or 'unknown-service'} {log.message}"
        for log in logs
    ]
    prompt = (
        "Summarize the likely incident, primary impact, recurring patterns, and recommended next actions from these error logs:\n"
        + "\n".join(bullet_lines)
    )
    response = client.responses.create(
        model=model,
        input=prompt,
    )
    return response.output_text
