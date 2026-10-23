import os
from datetime import datetime, timedelta, timezone

from google.cloud import logging_v2


def _parse_time(value: str | None, default: datetime) -> datetime:
    if not value:
        return default
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def query_error_logs() -> list[dict]:
    severity = os.getenv("LOG_SEVERITY", "ERROR").upper()
    end_time = _parse_time(os.getenv("END_TIME"), datetime.now(timezone.utc))
    start_default = end_time - timedelta(hours=1)
    start_time = _parse_time(os.getenv("START_TIME"), start_default)
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT")
    client = logging_v2.Client(project=project_id)
    logger = client.logger("_Default")
    filter_expr = (
        f'severity>="{severity}" '
        f'AND timestamp>="{start_time.isoformat()}" '
        f'AND timestamp<="{end_time.isoformat()}"'
    )
    entries = client.list_entries(filter_=filter_expr, order_by=logging_v2.DESCENDING)
    results: list[dict] = []
    for entry in entries:
        payload = entry.payload
        if isinstance(payload, dict):
            message = payload
        else:
            message = {"message": str(payload)}
        results.append(
            {
                "timestamp": entry.timestamp.isoformat() if entry.timestamp else None,
                "severity": str(entry.severity),
                "log_name": entry.log_name,
                "resource_type": entry.resource.type if entry.resource else None,
                "payload": message,
            }
        )
    return results


if __name__ == "__main__":
    for item in query_error_logs():
        print(item)
