from __future__ import annotations

from openai import OpenAI

from observability_client import build_openai_client
from observability_models import IncidentSummaryRequest


def summarize_incident(client: OpenAI, request: IncidentSummaryRequest) -> str:
    prompt = (
        f"Summarize the incident for review. Severity: {request.severity}. "
        f"Window: {request.time_window_minutes} minutes. Findings: {request.findings}"
    )
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": "You are an incident reviewer for operational logs."},
            {"role": "user", "content": prompt},
        ],
    )
    return response.id


def main() -> None:
    client = build_openai_client()
    request = IncidentSummaryRequest(
        severity="ERROR",
        time_window_minutes=60,
        findings=["Spike in 5xx responses", "Checkout latency increased", "Payment retries observed"],
    )
    summarize_incident(client, request)


if __name__ == "__main__":
    main()
