import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from google.cloud import logging_v2


def fetch_recent_logs(
    field_filters: Dict[str, str],
    start_time: datetime,
    end_time: Optional[datetime] = None,
    limit: int = 100,
) -> List[Dict[str, Any]]:
    client = logging_v2.Client()
    end_time = end_time or datetime.now(timezone.utc)
    if start_time.tzinfo is None:
        start_time = start_time.replace(tzinfo=timezone.utc)
    if end_time.tzinfo is None:
        end_time = end_time.replace(tzinfo=timezone.utc)

    filter_parts = [
        f'timestamp>="{start_time.isoformat()}"',
        f'timestamp<="{end_time.isoformat()}"',
    ]
    for field, value in field_filters.items():
        escaped = value.replace('"', '\\"')
        filter_parts.append(f'{field}="{escaped}"')

    iterator = client.list_entries(filter_=" AND ".join(filter_parts), page_size=limit)
    results: List[Dict[str, Any]] = []
    for entry in iterator:
        payload = entry.payload
        if hasattr(payload, "items"):
            payload = dict(payload)
        results.append(
            {
                "timestamp": entry.timestamp.isoformat() if entry.timestamp else None,
                "severity": getattr(entry, "severity", None),
                "log_name": entry.log_name,
                "resource": dict(entry.resource) if entry.resource else None,
                "payload": payload,
            }
        )
        if len(results) >= limit:
            break
    return results


if __name__ == "__main__":
    recent = fetch_recent_logs(
        field_filters={"severity": "ERROR"},
        start_time=datetime.now(timezone.utc) - timedelta(hours=1),
    )
    print(recent)
