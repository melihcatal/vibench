import os
from google.cloud import logging
from observability_models import build_structured_payload
from observability_client import get_project_id

def write_structured_log():
    project = get_project_id()
    client = logging.Client(project=project)
    logger = client.logger('structured-logs')
    payload = build_structured_payload('INFO', 'Structured log event written to Google Cloud Logging', app='web', version='1.0', event_type='user_action')
    logger.log_struct(payload)

if __name__ == "__main__":
    write_structured_log()