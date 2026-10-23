from observability_client import get_logger
from observability_models import CorrelatedLogEntry
from typing import List


def write_correlated_logs(
    log_entries: List[CorrelatedLogEntry], log_name: str = "application-logs"
):
    logger = get_logger(log_name)
    for entry in log_entries:
        payload = {
            "message": entry.message,
            "severity": entry.severity,
            "correlation_id": entry.correlation_id,
            **entry.metadata,
        }
        logger.log_struct(payload, severity=entry.severity)
