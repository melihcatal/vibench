from observability_client import get_logging_client
from observability_models import CorrelatedLogEntry

def write_correlated_logs(entries: list[CorrelatedLogEntry], log_name: str = "my-correlated-app-log"):
    logging_client = get_logging_client()
    logger = logging_client.logger(log_name)

    for entry in entries:
        resource = {
            "type": "global",
            "labels": {}
        }
        
        all_labels = entry.labels.copy()
        all_labels["correlation_id"] = entry.correlation_id

        if entry.json_payload:
            logger.log_struct(
                json_payload=entry.json_payload,
                severity=entry.severity,
                labels=all_labels,
                resource=resource
            )
        else:
            logger.log_text(
                text=entry.message,
                severity=entry.severity,
                labels=all_labels,
                resource=resource
            )
