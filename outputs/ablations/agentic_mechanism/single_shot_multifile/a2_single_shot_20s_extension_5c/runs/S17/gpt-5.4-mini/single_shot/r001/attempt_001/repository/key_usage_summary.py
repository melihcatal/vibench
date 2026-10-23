from __future__ import annotations

from typing import Any, Dict, List

from google.cloud import logging_v2

from security_client import get_project_id


def key_usage_summary(hours: int = 24) -> Dict[str, Any]:
    client = logging_v2.LoggingServiceV2Client()
    project_id = get_project_id()
    parent = f"projects/{project_id}"
    query = f'resource.type="cloud_kms_key" AND timestamp>="-{hours}h"'
    entries: List[Dict[str, Any]] = []
    for entry in client.list_log_entries(request={"resource_names": [parent], "filter": query}):
        entries.append({"timestamp": str(entry.timestamp), "severity": entry.severity.name, "message": entry.text_payload})
    return {"provider": "google-cloud-logging", "project_id": project_id, "hours": hours, "events": entries, "count": len(entries)}
