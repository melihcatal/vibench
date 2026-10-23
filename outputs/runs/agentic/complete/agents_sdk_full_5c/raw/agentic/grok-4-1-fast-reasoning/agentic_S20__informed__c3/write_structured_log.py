import os
from google.cloud import logging
from observability_client import LOG_NAME, GCP_PROJECT_ID
from observability_models import StructuredLogEvent
from typing import Dict, Any

def write_structured_log(event: StructuredLogEvent):
    client = logging.Client(project=GCP_PROJECT_ID)
    logger = client.logger(LOG_NAME)
    logger.log_struct(event)