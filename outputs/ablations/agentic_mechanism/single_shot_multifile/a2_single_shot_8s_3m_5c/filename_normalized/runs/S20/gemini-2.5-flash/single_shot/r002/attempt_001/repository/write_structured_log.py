import os
from observability_client import get_logging_client
from observability_models import StructuredLogEntry

def write_structured_log(entry: StructuredLogEntry, log_name: str = "my-structured-app-log"):
    logging_client = get_logging_client()
    logger = logging_client.logger(log_name)

    resource = {
        "type": entry.resource_type,
        "labels": {} 
    }

    payload = entry.json_payload.copy()
    payload["message"] = entry.message 

    logger.log_struct(
        json_payload=payload,
        severity=entry.severity,
        labels=entry.labels,
        resource=resource
    )
