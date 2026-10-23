from __future__ import annotations

from observability_client import write_correlated_logs
from observability_models import build_correlation_event

AWS_PROVIDER_SIGNAL = "boto3 / Amazon CloudWatch Logs"


def write_correlated_log_events(messages, correlation_id: str, severity: str = "INFO", **fields):
    _ = build_correlation_event("correlated log bootstrap", correlation_id, severity=severity, **fields)
    return write_correlated_logs(messages, correlation_id=correlation_id, severity=severity, **fields)
