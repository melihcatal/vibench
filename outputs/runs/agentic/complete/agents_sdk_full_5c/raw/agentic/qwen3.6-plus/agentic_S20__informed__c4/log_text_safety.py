"""
Checks selected log message text for unsafe content.

Uses the Azure AI Content Safety API (api.cognitiveservices.azure.com)
to analyze log messages for hate, violence, sexual, and self-harm content.
Auth: AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY environment variables.
"""

import json
import os
from typing import Optional

import requests

AZURE_CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"


def get_azure_content_safety_endpoint() -> str:
    """Retrieve the Azure AI Content Safety endpoint from environment."""
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    if not endpoint:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT environment variable is required")
    return endpoint.rstrip("/")


def get_azure_content_safety_key() -> str:
    """Retrieve the Azure AI Content Safety key from environment."""
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    if not key:
        raise ValueError("AZURE_CONTENT_SAFETY_KEY environment variable is required")
    return key


def analyze_text_safety(text: str, blocklists: Optional[list[str]] = None) -> dict:
    """Analyze a single text string for unsafe content using Azure AI Content Safety.

    Sends a POST request to the Azure AI Content Safety API endpoint
    (api.cognitiveservices.azure.com) via the /text:analyze endpoint
    to evaluate text for hate, violence, sexual, and self-harm categories.
    """
    endpoint = get_azure_content_safety_endpoint()
    api_key = get_azure_content_safety_key()

    url = f"{endpoint}/contentsafety/text:analyze"
    params = {"api-version": AZURE_CONTENT_SAFETY_API_VERSION}

    payload = {
        "text": text,
        "categories": ["Hate", "Sexual", "SelfHarm", "Violence"],
        "outputType": "FourSeverityLevels",
    }

    if blocklists:
        payload["blocklists"] = [
            {"blocklistName": bl} for bl in blocklists
        ]

    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": api_key,
    }

    response = requests.post(url, headers=headers, params=params, json=payload)
    response.raise_for_status()
    return response.json()


def check_log_messages_safety(
    messages: list[dict],
) -> list[dict]:
    """Check a list of log messages for unsafe content via Azure Content Safety.

    Each message dict should contain at least a 'message' key with the text to analyze,
    and optionally 'timestamp', 'service', 'status' metadata.
    Results are returned with the original metadata plus the safety analysis.
    """
    results = []
    for msg_entry in messages:
        text = msg_entry.get("message", "")
        if not text:
            continue

        try:
            analysis = analyze_text_safety(text)
        except Exception as e:
            analysis = {"error": str(e)}

        result_entry = {
            "original": msg_entry,
            "safety_analysis": analysis,
        }

        if "error" not in analysis:
            categories = analysis.get("categoriesAnalysis", [])
            result_entry["flags"] = {
                cat.get("category", ""): cat.get("severity", 0)
                for cat in categories
            }
            result_entry["has_unsafe_content"] = any(
                cat.get("severity", 0) > 0
                for cat in categories
            )

        results.append(result_entry)

    return results


def format_safety_report(results: list[dict]) -> str:
    """Format a human-readable safety analysis report."""
    lines = [
        "Log Message Safety Report (Azure AI Content Safety)",
        "=" * 55,
        f"Messages analyzed: {len(results)}",
        "",
    ]

    flagged_count = 0
    for i, result in enumerate(results, 1):
        original = result.get("original", {})
        flags = result.get("flags", {})
        has_unsafe = result.get("has_unsafe_content", False)

        status_marker = "[FLAGGED]" if has_unsafe else "[CLEAN]"
        if has_unsafe:
            flagged_count += 1

        lines.append(f"[{i}] {status_marker}")
        lines.append(f"    Service: {original.get('service', 'unknown')}")
        lines.append(f"    Status: {original.get('status', 'unknown')}")
        lines.append(f"    Message: {original.get('message', '')[:120]}")

        if has_unsafe and flags:
            lines.append("    Content Safety Flags:")
            for category, severity in flags.items():
                if severity and severity > 0:
                    lines.append(f"      - {category}: severity {severity}")
        lines.append("")

    lines.append(f"Summary: {flagged_count}/{len(results)} messages flagged for unsafe content.")
    lines.append("=" * 55)
    return "\n".join(lines)


def main():
    """Entry point for checking log messages for unsafe content."""
    sample_messages = [
        {
            "message": "User reported issue with login functionality on production",
            "timestamp": "2025-01-15T10:00:00Z",
            "service": "auth-service",
            "status": "info",
        },
        {
            "message": "Error: unauthorized access attempt detected from suspicious IP range",
            "timestamp": "2025-01-15T10:05:00Z",
            "service": "api-gateway",
            "status": "warning",
        },
        {
            "message": "Database query completed successfully in 45ms",
            "timestamp": "2025-01-15T10:10:00Z",
            "service": "data-service",
            "status": "info",
        },
    ]

    results = check_log_messages_safety(sample_messages)

    report = format_safety_report(results)
    print(report)

    print("\n--- Raw JSON ---")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
