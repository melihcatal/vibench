from __future__ import annotations

from observability_client import write_structured_log
from observability_models import build_structured_event

AWS_PROVIDER_SIGNAL = "boto3 / Amazon CloudWatch Logs"


def write_structured_log_event(message: str, severity: str = "INFO", **fields):
    event = build_structured_event(message, severity=severity, **fields)
    return write_structured_log(event["message"], severity=event["severity"], **{k: v for k, v in event.items() if k not in {"message", "severity"}})
