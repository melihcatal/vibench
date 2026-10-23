import os
import datetime
from observability_client import ObservabilityClient
from observability_models import LogEntry


def fetch_recent_logs(
    field_filters: dict = None, time_range_minutes: int = 60
) -> list[dict]:
    client = ObservabilityClient()
    project_id = client.logging_client.project

    now = datetime.datetime.now(datetime.timezone.utc)
    past = now - datetime.timedelta(minutes=time_range_minutes)

    filter_parts = [
        f'resource.type="global" ',
        f'timestamp >= "{past.isoformat()}" ',
        f'timestamp <= "{now.isoformat()}" ',
    ]

    if field_filters:
        for field, value in field_filters.items():
            filter_parts.append(f'{field}="{value}"')

    filter_string = " AND ".join(filter_parts)

    entries = client.logging_client.list_entries(
        filter_=filter_string, order_by="timestamp desc", project_ids=[project_id]
    )

    results = []
    for entry in entries:
        results.append(LogEntry.from_gcp_entry(entry.to_api_repr()).to_dict())
    return results
