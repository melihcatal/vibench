from google.cloud import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any
from observability_client import get_google_cloud_project
from observability_models import LogQuery

def query_error_logs(hours_back: int = 24) -> List[Dict[str, Any]]:
    project = get_google_cloud_project()
    client = logging.Client(project=project)
    now = datetime.utcnow()
    start_time = now - timedelta(hours=hours_back)
    query = LogQuery(
        filter_str='severity >= "ERROR"',
        start_time=start_time,
        page_size=50
    )
    filter_str = query.build_filter()
    entries_it = client.list_entries(
        filter_=filter_str,
        order_by="TIMESTAMP"
    )
    entries = list(entries_it)[:query.page_size]
    return [entry.payload for entry in entries if hasattr(entry, 'payload') and entry.payload]
