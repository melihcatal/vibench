"""
Checks selected log message text for unsafe content using Azure AI Content Safety.
Provider: Azure AI Content Safety API
Auth: AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY
"""

import os
from typing import Dict, Any, List
import requests


def get_safety_endpoint() -> str:
    """Retrieve Azure Content Safety endpoint from environment."""
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    if not endpoint:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT environment variable is required")
    return endpoint.rstrip("/")


def get_safety_key() -> str:
    """Retrieve Azure Content Safety key from environment."""
    api_key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    if not api_key:
        raise ValueError("AZURE_CONTENT_SAFETY_KEY environment variable is required")
    return api_key


def check_log_text_safety(
    text: str,
    categories: List[str] = None,
) -> Dict[str, Any]:
    """Analyze log message text for unsafe content categories.

    Uses Azure AI Content Safety Text Analysis API to detect hate, self-harm,
    sexual, and violence categories in the provided text.
    """
    if categories is None:
        categories = ["Hate", "SelfHarm", "Sexual", "Violence"]

    endpoint = get_safety_endpoint()
    api_key = get_safety_key()
    url = f"{endpoint}/contentsafety/text:analyze?api-version=2024-02-15-preview"

    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json",
    }
    body = {
        "text": text,
        "categories": categories,
    }

    response = requests.post(url, headers=headers, json=body, timeout=30)
    response.raise_for_status()
    return response.json()


def scan_log_messages_for_safety(
    messages: List[str],
) -> List[Dict[str, Any]]:
    """Scan a list of log messages and return safety analysis for each."""
    results = []
    for msg in messages:
        result = check_log_text_safety(msg)
        results.append({
            "text": msg,
            "safety_result": result,
        })
    return results


def is_text_flagged(safety_result: Dict[str, Any]) -> bool:
    """Check if any category in the safety result exceeds the safe threshold."""
    categories = safety_result.get("categoriesAnalysis", [])
    for cat in categories:
        if cat.get("severity", 0) >= 4:
            return True
    return False


if __name__ == "__main__":
    sample_messages = [
        "User submitted invalid credentials for account login",
        "Warning: detected abusive language in user feedback field",
    ]
    results = scan_log_messages_for_safety(sample_messages)
    for r in results:
        flagged = is_text_flagged(r["safety_result"])
        print(f"[{'FLAGGED' if flagged else 'CLEAN'}] {r['text']}")
        print(r["safety_result"])
