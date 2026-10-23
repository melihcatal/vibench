import os
import json
from typing import Dict, Any, List
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def check_log_safety(log_messages: List[str]) -> Dict[str, Any]:
    """Check selected log message text for unsafe content using Azure AI Content Safety."""

    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "Azure Content Safety endpoint and key must be set in environment variables"
        )

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    results = []

    for message in log_messages:
        if not message or not isinstance(message, str):
            results.append(
                {
                    "message": message,
                    "safe": True,
                    "categories": {},
                    "error": "Invalid message format",
                }
            )
            continue

        request = AnalyzeTextOptions(text=message)

        try:
            response = client.analyze_text(request)

            category_scores = {}
            is_safe = True

            for category_result in response.categories_analysis:
                category_name = category_result.category.value
                severity = category_result.severity
                category_scores[category_name] = severity

                if severity > 0:
                    is_safe = False

            results.append(
                {
                    "message": message,
                    "safe": is_safe,
                    "categories": category_scores,
                    "blocklists_matched": [
                        {
                            "blocklist_name": match.blocklist_name,
                            "blocklist_item_id": match.blocklist_item_id,
                            "blocklist_item_text": match.blocklist_item_text,
                        }
                        for match in response.blocklists_match
                    ]
                    if hasattr(response, "blocklists_match")
                    else [],
                }
            )

        except Exception as e:
            results.append(
                {
                    "message": message,
                    "safe": False,
                    "categories": {},
                    "error": f"Azure Content Safety API error: {str(e)}",
                }
            )

    summary = {
        "total_messages": len(log_messages),
        "safe_messages": sum(1 for r in results if r.get("safe", False)),
        "unsafe_messages": sum(1 for r in results if not r.get("safe", True)),
        "categories_found": {},
        "results": results,
    }

    for result in results:
        for category, severity in result.get("categories", {}).items():
            if severity > 0:
                if category not in summary["categories_found"]:
                    summary["categories_found"][category] = 0
                summary["categories_found"][category] += 1

    return summary


def filter_unsafe_logs(log_entries: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Filter log entries for unsafe content and return safe/unsafe categorization."""

    messages = [entry.get("message", "") for entry in log_entries]

    safety_results = check_log_safety(messages)

    safe_logs = []
    unsafe_logs = []

    for i, result in enumerate(safety_results["results"]):
        log_entry = (
            log_entries[i] if i < len(log_entries) else {"message": result["message"]}
        )

        if result.get("safe", False):
            safe_logs.append(log_entry)
        else:
            unsafe_entry = log_entry.copy()
            unsafe_entry["safety_issues"] = {
                "categories": result.get("categories", {}),
                "blocklists_matched": result.get("blocklists_matched", []),
                "error": result.get("error"),
            }
            unsafe_logs.append(unsafe_entry)

    return {
        "total_logs": len(log_entries),
        "safe_logs": safe_logs,
        "unsafe_logs": unsafe_logs,
        "safety_summary": {
            "safe_count": len(safe_logs),
            "unsafe_count": len(unsafe_logs),
            "categories_found": safety_results.get("categories_found", {}),
        },
    }


if __name__ == "__main__":
    test_logs = [
        {"message": "User authentication successful", "severity": "INFO"},
        {"message": "Database connection error: timeout", "severity": "ERROR"},
        {"message": "Invalid input received from user", "severity": "WARNING"},
        {"message": "System shutdown initiated", "severity": "INFO"},
    ]

    result = filter_unsafe_logs(test_logs)
    print(f"Total logs: {result['total_logs']}")
    print(f"Safe logs: {result['safety_summary']['safe_count']}")
    print(f"Unsafe logs: {result['safety_summary']['unsafe_count']}")

    if result["safety_summary"]["categories_found"]:
        print("Categories found:", result["safety_summary"]["categories_found"])
