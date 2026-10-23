from observability_client import get_logger
from observability_models import StructuredLogEntry


def write_structured_log(
    log_entry: StructuredLogEntry, log_name: str = "application-logs"
):
    logger = get_logger(log_name)
    payload = {
        "message": log_entry.message,
        "severity": log_entry.severity,
        **log_entry.metadata,
    }
    logger.log_struct(payload, severity=log_entry.severity)
