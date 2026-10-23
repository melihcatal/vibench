from observability_client import get_logging_client, get_project_id
from observability_models import ErrorLogQuery
from datetime import datetime, timedelta


def query_error_logs(query: ErrorLogQuery) -> List[Dict]:
    client = get_logging_client()
    project_id = query.project_id if query.project_id else get_project_id()

    now = datetime.utcnow()
    time_threshold = now - timedelta(minutes=query.time_range_minutes)

    # Construct the filter string
    filter_str = f'severity >= {query.min_severity} AND timestamp >= "{time_threshold.isoformat("T")}"'

    entries = client.list_entries(filter_=filter_str, project_ids=[project_id])

    results = []
    for entry in entries:
        results.append(entry.to_api_repr())
    return results
