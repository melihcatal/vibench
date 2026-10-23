import os
import uuid
from google.cloud import logging
from observability_client import get_logging_client

def write_correlated_logs(log_name: str, messages: list[str], severity: str = 'INFO', correlation_id: str = None):
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    client = get_logging_client()
    logger = client.logger(log_name)

    if correlation_id is None:
        correlation_id = str(uuid.uuid4())

    for i, message in enumerate(messages):
        entry = {
            "message": message,
            "correlation_id": correlation_id,
            "sequence": i + 1
        }
        logger.log_struct(
            entry,
            severity=severity,
            resource=logging.resource.Resource(type='global', labels={'project_id': project_id})
        )

