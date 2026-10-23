import os
import datetime
from observability_client import ObservabilityClient
from observability_models import LogEntry


def query_error_logs(
    severity: str = "ERROR", time_range_minutes: int = 60
) -> list[dict]:
    client = ObservabilityClient()
    project_id = client.logging_client.project

    now = datetime.datetime.now(datetime.timezone.utc)
    past = now - datetime.timedelta(minutes=time_range_minutes)

    filter_string = (
        f'resource.type="global" AND severity="{severity}" '
        f'AND timestamp >= "{past.isoformat()}" '
        f'AND timestamp <= "{now.isoformat()}" '
    )

    entries = client.logging_client.list_entries(
        filter_=filter_string, order_by="timestamp desc", project_ids=[project_id]
    )

    results = []
    for entry in entries:
        results.append(LogEntry.from_gcp_entry(entry.to_api_repr()).to_dict())
    return results
