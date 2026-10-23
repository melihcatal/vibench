import os
from google.cloud import logging
from typing import List, Dict, Any
from observability_models import format_time
from observability_client import get_project_id

def query_error_logs(days_back: int = 1) -> List[Dict[str, Any]]:
    project = get_project_id()
    client = logging.Client(project=project)
    start_time = format_time(days_back)
    filter_str = f'severity >= "ERROR" AND timestamp >= "{start_time}"'
    entries = client.list_entries(filter_=filter_str)
    logs = []
    for entry in entries:
        payload = dict(entry.json_payload) if entry.json_payload else {'text': entry.text_payload}
        log = {
            'timestamp': str(entry.timestamp),
            'severity': entry.severity,
            'payload': payload,
        }
        logs.append(log)
    return logs

if __name__ == "__main__":
    errors = query_error_logs()
    print(f"Recent error logs: {len(errors)}")