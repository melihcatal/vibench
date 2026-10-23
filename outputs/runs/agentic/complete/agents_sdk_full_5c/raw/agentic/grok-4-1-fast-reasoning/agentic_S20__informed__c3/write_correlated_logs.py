import os
from google.cloud import logging
from typing import List
from observability_client import LOG_NAME, GCP_PROJECT_ID
from observability_models import StructuredLogEvent

def write_correlated_logs(correlation_id: str, logs: List[StructuredLogEvent]):
    client = logging.Client(project=GCP_PROJECT_ID)
    logger = client.logger(LOG_NAME)
    for log in logs:
        log_copy = log.copy()
        log_copy.setdefault("correlation_id", correlation_id)
        logger.log_struct(log_copy)