import os
from observability_client import ObservabilityClient
from observability_models import LogEntry

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
if not PROJECT_ID:
    raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set")

def write_correlated_logs(log_entries: list[LogEntry], correlation_id: str):
    client = ObservabilityClient(project_id=PROJECT_ID)
    logger = client.get_logger()

    for entry in log_entries:
        # Ensure correlation_id is set for each entry
        entry.correlation_id = correlation_id
        
        log_data = {
            "message": entry.message,
            "severity": entry.severity.value,
            "correlation_id": entry.correlation_id,
        }
        if entry.json_payload:
            log_data.update(entry.json_payload)

        logger.log_struct(
            log_data,
            severity=entry.severity.value,
            resource={
                "type": entry.resource_type,
                "labels": entry.resource_labels
            }
        )
    return {"submitted": True}
