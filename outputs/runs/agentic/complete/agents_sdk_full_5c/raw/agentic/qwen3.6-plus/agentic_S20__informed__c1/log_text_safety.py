"""Check selected log message text for unsafe content using Azure AI Content Safety."""

import json
import os
from typing import Dict, List, Optional

import requests

from observability_models import LogEntry


def check_log_text_safety(
    log_messages: List[str],
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> dict:
    """Check selected log message text for unsafe content using Azure AI Content Safety.

    Uses the Azure AI Content Safety REST API (azure-ai-contentsafety compatible)
    with AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY for
    authentication. Calls the /contentsafety/text:analyze endpoint to detect
    hate, self-harm, sexual, and violent content in log messages.
    """
    content_safety_endpoint = endpoint or os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    content_safety_key = api_key or os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not content_safety_endpoint or not content_safety_key:
        raise ValueError(
            "Azure AI Content Safety credentials required. Set "
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY."
        )

    # Ensure endpoint does not have trailing slash
    base_url = content_safety_endpoint.rstrip("/")
    api_version = "2024-02-15-preview"
    url = f"{base_url}/contentsafety/text:analyze?api-version={api_version}"

    headers = {
        "Ocp-Apim-Subscription-Key": content_safety_key,
        "Content-Type": "application/json",
    }

    results = []
    for i, message in enumerate(log_messages):
        payload = {
            "text": message,
            "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
            "outputType": "FourSeverityLevels",
        }

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        analysis = response.json()

        category_scores = {}
        flagged = False
        for cat in analysis.get("categoriesAnalysis", []):
            category = cat.get("category", "Unknown")
            severity = cat.get("severity", 0)
            category_scores[category] = severity
            if severity > 0:
                flagged = True

        results.append({
            "index": i,
            "text_preview": message[:120],
            "flagged": flagged,
            "category_scores": category_scores,
        })

    return {
        "provider": "Azure AI Content Safety",
        "endpoint": base_url,
        "api_version": api_version,
        "messages_checked": len(log_messages),
        "flagged_count": sum(1 for r in results if r["flagged"]),
        "results": results,
    }


def check_log_entries_safety(
    log_entries: List[LogEntry],
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> dict:
    """Extract messages from log entries and check them for unsafe content."""
    messages = [str(entry.message) for entry in log_entries if entry.message]
    return check_log_text_safety(messages, endpoint=endpoint, api_key=api_key)


def main():
    sample_messages = [
        "User login successful from IP 192.168.1.100",
        "Failed to connect to database: connection refused",
        "Payment processed successfully for order #12345",
    ]

    result = check_log_text_safety(sample_messages)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
