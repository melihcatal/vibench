import os
import datetime
from google.cloud import logging
from observability_client import get_logging_client

def write_structured_log(log_name: str, payload: dict, severity: str = 'INFO'):
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    client = get_logging_client()
    logger = client.logger(log_name)

    # The structured log entry is automatically placed in jsonPayload
    logger.log_struct(
        payload,
        severity=severity,
        resource=logging.resource.Resource(type='global', labels={'project_id': project_id})
    )

