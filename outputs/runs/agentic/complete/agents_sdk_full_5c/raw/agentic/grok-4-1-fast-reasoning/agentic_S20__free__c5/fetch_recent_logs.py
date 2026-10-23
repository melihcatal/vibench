from google.cloud import logging
from observability_client import PROJECT_ID, LOGGER_NAME
from observability_models import get_service_log_filter
import json

def fetch_recent_logs(service_name='user-service'):
    client = logging.Client(project=PROJECT_ID)
    log_filter = f'logName="projects/{PROJECT_ID}/logs/{LOGGER_NAME}" {get_service_log_filter(service_name)}'
    entries = []
    page_iterator = client.list_entries(filter_=log_filter, page_size=50)
    for entry in page_iterator:
        entries.append({
            'timestamp': str(entry.timestamp),
            'json_payload': dict(entry.json_payload) if entry.json_payload else None
        })
        if len(entries) &gt;= 10:
            break
    print(json.dumps(entries, default=str, indent=2))

if __name__ == '__main__':
    fetch_recent_logs()