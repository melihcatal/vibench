import os
import json
import requests
from observability_client import get_bing_tenant_id, get_bing_key


def is_log_text_safe(log_text: str) -> bool:
    """Check whether a single log message contains unsafe content using Azure Content Safety API.",
    Returns True if safe, False if unsafe.",
    Raises:
        RuntimeError for HTTP errors.",
    """
    endpoint = f"https://{get_bing_tenant_id()}.api.security.azure.com/api/content-safety/v1.0/textModeration"
    headers = {"Content-Type": "application/json", "api-key": get_bing_key()}
    payload = {"inputText": log_text}
    resp = requests.post(endpoint, headers=headers, json=payload)
    resp.raise_for_status()
    result = resp.json()
    # Example Azure response: {"results": [{"category": "safe", "detail": {}}]}
    categories = [mod["category"] for mod in result.get("results", [])]
    return "unsafe" not in categories.lower()
