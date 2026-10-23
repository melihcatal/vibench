from datetime import datetime, timedelta, timezone

from observability_client import ObservabilityClient
from observability_models import QueryFilter

def fetch_recent_logs(time_range_minutes=60, field_filters=None, text_search=None, config=None):
    config = config or {}
    client = ObservabilityClient(project_id=config["project_id"])
    logging_client = client.get_logging_client()

    now = datetime.now(timezone.utc)
    time_range_start = now - timedelta(minutes=time_range_minutes)

    query_filter = QueryFilter(
        time_range_start=time_range_start,
        time_range_end=now,
        text_search=text_search,
        fields=field_filters
    )

    filter_string = query_filter.to_filter_string()
    entries = logging_client.list_entries(filter_=filter_string, projects=[config["project_id"]])

    results = []
    for entry in entries:
        results.append({
            "timestamp": entry.timestamp.isoformat(),
            "severity": entry.severity,
            "payload": entry.payload,
            "log_name": entry.log_name,
        })
    return {"logs": results}
