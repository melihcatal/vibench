import os
import sys
import json
import requests
from typing import Optional

from observability_models import LogEntry


AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get(
    "AZURE_CONTENT_SAFETY_ENDPOINT",
    "https://<your-resource>.cognitiveservices.azure.com/",
)
AZURE_CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"


def check_log_text_safety(
    text: str,
    categories: Optional[list[str]] = None,
) -> dict:
    if not categories:
        categories = ["Hate", "SelfHarm", "Sexual", "Violence"]

    endpoint = AZURE_CONTENT_SAFETY_ENDPOINT.rstrip("/")
    url = f"{endpoint}/contentsafety/text:analyze"

    params = {"api-version": AZURE_CONTENT_SAFETY_API_VERSION}
    headers = {
        "Ocp-Apim-Subscription-Key": os.environ["AZURE_CONTENT_SAFETY_KEY"],
        "Content-Type": "application/json",
    }
    body = {
        "text": text,
        "categories": categories,
        "outputType": "FourSeverityLevels",
    }

    response = requests.post(url, headers=headers, params=params, json=body, timeout=30)
    response.raise_for_status()
    return response.json()


def check_log_entries_safety(
    entries: list[LogEntry],
    categories: Optional[list[str]] = None,
) -> list[dict]:
    results = []
    for entry in entries:
        if not entry.message.strip():
            continue
        safety_result = check_log_text_safety(entry.message, categories=categories)
        results.append(
            {
                "log_id": entry.id,
                "timestamp": entry.timestamp,
                "service": entry.service,
                "message_preview": entry.message[:200],
                "safety_analysis": safety_result,
                "has_unsafe_content": any(
                    cat.get("severity", 0) > 0
                    for cat in safety_result.get("categoriesAnalysis", [])
                ),
            }
        )
    return results


def main():
    log_file = sys.argv[1] if len(sys.argv) > 1 else ""

    if log_file:
        with open(log_file, "r") as f:
            data = json.load(f)
        entries = [LogEntry(**e) for e in data.get("entries", [])]
    else:
        entries = [
            LogEntry(
                id="log-1",
                timestamp="2026-04-21T10:00:00Z",
                message="User submitted feedback: great service!",
                severity="info",
                service="feedback-service",
            ),
            LogEntry(
                id="log-2",
                timestamp="2026-04-21T10:01:00Z",
                message="Input validation failed for request payload",
                severity="warning",
                service="api-gateway",
            ),
        ]

    safety_results = check_log_entries_safety(entries)
    print(json.dumps(safety_results, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
