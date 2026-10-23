from google.cloud import logging_v2
from datetime import datetime, timezone

def fetch_recent_logs(config, field, value, start_time, end_time):
    client = logging_v2.Client(project=config["project_id"])
    logger = client.logger(config["log_name"])
    filter_ = f'{field}={value} AND timestamp>="{start_time.isoformat()}" AND timestamp<="{end_time.isoformat()}"'
    entries = logger.list_entries(filter_=filter_)
    return [entry.payload.fields for entry in entries]