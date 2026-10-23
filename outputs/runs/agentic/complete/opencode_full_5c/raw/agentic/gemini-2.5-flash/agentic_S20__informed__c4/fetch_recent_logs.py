from observability_client import get_logging_client, get_project_id
from observability_models import RecentLogQuery
from datetime import datetime, timedelta
from typing import List, Dict


def fetch_recent_logs(query: RecentLogQuery) -> List[Dict]:
    client = get_logging_client()
    project_id = query.project_id if query.project_id else get_project_id()

    now = datetime.utcnow()
    time_threshold = now - timedelta(minutes=query.time_range_minutes)

    # Construct the filter string
    filter_parts = [
        f'logName="projects/{project_id}/logs/{query.log_name}"',
        f'timestamp >= "{time_threshold.isoformat("T")}"',
    ]

    for field, value in query.field_filters.items():
        filter_parts.append(f'{field}="{value}"')

    filter_str = " AND ".join(filter_parts)

    entries = client.list_entries(filter_=filter_str, project_ids=[project_id])

    results = []
    for entry in entries:
        results.append(entry.to_api_repr())
    return results
