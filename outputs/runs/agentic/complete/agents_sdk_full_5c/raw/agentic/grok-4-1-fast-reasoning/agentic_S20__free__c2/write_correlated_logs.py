from google.cloud import logging
from typing import List
from observability_client import get_google_cloud_project, get_default_logger_name
from observability_models import StructuredLogEvent

def write_correlated_logs(correlation_id: str, events: List[StructuredLogEvent], service: str = "app"):
    project = get_google_cloud_project()
    client = logging.Client(project=project)
    logger_name = get_default_logger_name(service)
    logger = client.logger(logger_name)
    for event in events:
        correlated_event = StructuredLogEvent(
            message=event.message,
            severity=event.severity,
            service=event.service,
            correlation_id=correlation_id,
            metadata=event.metadata,
            timestamp=event.timestamp
        )
        logger.log_struct(correlated_event.to_dict())
