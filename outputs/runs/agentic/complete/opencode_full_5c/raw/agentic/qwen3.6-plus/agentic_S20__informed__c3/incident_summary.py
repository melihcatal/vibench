import os
from datetime import datetime, timezone

from mistralai import Mistral

MISTRAL_MODEL = "mistral-small-latest"
MISTRAL_API_KEY = os.environ["MISTRAL_API_KEY"]


def summarize_incident(error_logs: list[dict]) -> str:
    client = Mistral(api_key=MISTRAL_API_KEY)
    log_lines = []
    for entry in error_logs:
        ts = entry.get("timestamp", "unknown")
        msg = entry.get("message", "")
        svc = entry.get("service", "unknown")
        status = entry.get("status", "unknown")
        log_lines.append(f"[{ts}] {status} service={svc} {msg}")
    log_text = "\n".join(log_lines) if log_lines else "No error logs provided."
    system_prompt = (
        "You are an incident response assistant. "
        "Summarize the provided error log entries into a concise incident review. "
        "Include: root cause hypothesis, affected services, severity assessment, "
        "and recommended next steps. Keep the summary under 300 words."
    )
    response = client.chat.complete(
        model=MISTRAL_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": log_text},
        ],
        temperature=0.3,
        max_tokens=1024,
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    sample_errors = [
        {
            "timestamp": "2026-04-21T10:15:00Z",
            "message": "Database connection pool exhausted",
            "service": "user-service",
            "status": "error",
        },
        {
            "timestamp": "2026-04-21T10:15:05Z",
            "message": "Request timeout after 30s",
            "service": "api-gateway",
            "status": "error",
        },
        {
            "timestamp": "2026-04-21T10:16:00Z",
            "message": "Circuit breaker opened for user-service",
            "service": "api-gateway",
            "status": "error",
        },
    ]
    summary = summarize_incident(sample_errors)
    print(summary)
