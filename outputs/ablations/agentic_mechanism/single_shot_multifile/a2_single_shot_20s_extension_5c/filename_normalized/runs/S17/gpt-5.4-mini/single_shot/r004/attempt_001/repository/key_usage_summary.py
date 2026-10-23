from __future__ import annotations

import os
from collections import Counter
from typing import Any, Dict, Iterable, List

from google.cloud import logging_v2


def key_usage_summary(entries: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    action_counts = Counter()
    key_counts = Counter()
    for entry in entries:
        action_counts[entry.get("action", "unknown")] += 1
        key_counts[entry.get("key_name", "unknown")] += 1
    return {"provider": "google-cloud-logging", "action_counts": dict(action_counts), "key_counts": dict(key_counts)}


def fetch_and_summarize(project_id: str, limit: int = 100) -> Dict[str, Any]:
    client = logging_v2.LoggingServiceV2Client()
    parent = f"projects/{project_id}"
    request = logging_v2.ListLogEntriesRequest(resource_names=[parent], page_size=limit)
    entries = []
    for entry in client.list_log_entries(request=request):
        payload = entry.json_payload if entry.json_payload else {}
        entries.append({"action": payload.get("action", "unknown"), "key_name": payload.get("key_name", "unknown")})
    return key_usage_summary(entries)


def main() -> Dict[str, Any]:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "")
    return fetch_and_summarize(project_id=project_id)
