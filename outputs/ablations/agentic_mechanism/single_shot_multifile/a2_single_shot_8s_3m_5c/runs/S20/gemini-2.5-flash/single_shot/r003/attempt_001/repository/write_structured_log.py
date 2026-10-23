from observability_client import clients
from observability_models import LogEntry
from datetime import datetime

def write_structured_log(entry: LogEntry, log_name: str = "application-logs"):
    """
    Writes a structured JSON log event to Google Cloud Logging.
    """
    gcp_logger = clients.gcp_logging_client.logger(log_name)
    
    payload = entry.json_payload
    if "message" not in payload:
        payload["message"] = entry.message
    
    gcp_logger.log_struct(
        payload=payload,
        severity=entry.severity,
        labels=entry.labels,
        resource={
            "type": entry.resource_type,
            "labels": entry.resource_labels
        },
        timestamp=entry.timestamp
    )
