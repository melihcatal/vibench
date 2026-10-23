from google.cloud import logging_v2
from google.protobuf.timestamp_pb2 import Timestamp
import datetime

def fetch_recent_logs(project_id: str, log_filter: str, start_time: datetime.datetime, end_time: datetime.datetime):
    client = logging_v2.client.LoggingClient()

    # Convert datetime objects to RFC3339 strings for the filter
    start_time_str = start_time.isoformat("T") + "Z"
    end_time_str = end_time.isoformat("T") + "Z"

    full_filter = f'''timestamp >= "{start_time_str}" AND timestamp < "{end_time_str}"'''
    if log_filter:
        full_filter = f"{full_filter} AND ({log_filter})"

    entries = client.list_log_entries(
        request={
            "project_ids": [project_id],
            "filter": full_filter,
            "order_by": "timestamp desc",
        }
    )

    log_results = []
    for entry in entries:
        log_results.append(entry)
    return log_results
