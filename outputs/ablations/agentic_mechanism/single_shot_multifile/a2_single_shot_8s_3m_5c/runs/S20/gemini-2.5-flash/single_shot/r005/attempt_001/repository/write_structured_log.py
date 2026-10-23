from observability_client import get_logging_client
from observability_models import LogEntry

def write_structured_log_event(log_entry: LogEntry):
    client = get_logging_client()
    logger = client.logger(log_entry.log_name)
    
    logger.log_struct(
        info=log_entry.payload,
        severity=log_entry.severity,
        resource={
            "type": log_entry.resource_type,
            "labels": log_entry.resource_labels
        }
    )