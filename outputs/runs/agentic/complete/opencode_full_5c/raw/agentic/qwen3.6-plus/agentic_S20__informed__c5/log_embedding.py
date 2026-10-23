import os
import sys
import json
from typing import Optional

from openai import OpenAI

from observability_models import LogEntry


def embed_log_messages(
    messages: list[str],
    model: str = "text-embedding-3-small",
) -> list[list[float]]:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    response = client.embeddings.create(
        model=model,
        input=messages,
    )

    sorted_embeddings = sorted(response.data, key=lambda x: x.index)
    return [emb.embedding for emb in sorted_embeddings]


def embed_log_entries(
    entries: list[LogEntry],
    model: str = "text-embedding-3-small",
) -> list[dict]:
    messages = [entry.message for entry in entries if entry.message.strip()]
    if not messages:
        return []

    embeddings = embed_log_messages(messages, model=model)

    results = []
    for entry, embedding in zip(
        [e for e in entries if e.message.strip()],
        embeddings,
    ):
        results.append(
            {
                "log_id": entry.id,
                "timestamp": entry.timestamp,
                "service": entry.service,
                "severity": entry.severity,
                "message": entry.message,
                "embedding_model": model,
                "embedding_dimension": len(embedding),
                "embedding": embedding,
            }
        )
    return results


def main():
    log_file = sys.argv[1] if len(sys.argv) > 1 else ""
    model = sys.argv[2] if len(sys.argv) > 2 else "text-embedding-3-small"

    if log_file:
        with open(log_file, "r") as f:
            data = json.load(f)
        entries = [LogEntry(**e) for e in data.get("entries", [])]
    else:
        entries = [
            LogEntry(
                id="log-1",
                timestamp="2026-04-21T10:00:00Z",
                message="Connection pool exhausted, unable to acquire database connection",
                severity="error",
                service="api-gateway",
            ),
            LogEntry(
                id="log-2",
                timestamp="2026-04-21T10:01:00Z",
                message="Payment processing timeout after 30 seconds",
                severity="critical",
                service="payment-service",
            ),
            LogEntry(
                id="log-3",
                timestamp="2026-04-21T10:02:00Z",
                message="Retry limit exceeded for external API call",
                severity="error",
                service="notification-service",
            ),
        ]

    results = embed_log_entries(entries, model=model)
    print(json.dumps(results, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
