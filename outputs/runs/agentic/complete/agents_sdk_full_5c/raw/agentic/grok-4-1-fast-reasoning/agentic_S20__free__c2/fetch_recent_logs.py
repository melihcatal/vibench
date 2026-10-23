from google.cloud import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any
from observability_client import get_google_cloud_project
from observability_models import LogQuery

def fetch_recent_logs(field_filter: str, field_value: str, hours_back: int = 1) -> List[Dict[str, Any]]:
    project = get_google_cloud_project()
    client = logging.Client(project=project)
    now = datetime.utcnow()
    start_time = now - timedelta(hours=hours_back)
    filter_str = f'jsonPayload.{field_filter} = "{field_value}"'
    query = LogQuery(filter_str=filter_str, start_time=start_time)
    full_filter = query.build_filter()
    entries_it = client.list_entries(
        filter_=full_filter,
        order_by="TIMESTAMP"
    )
    entries = list(entries_it)[:100]
    return [entry.payload for entry in entries if hasattr(entry, 'payload') and entry.payload]
