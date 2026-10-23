from observability_client import DatadogLogsClient
from observability_models import build_log_record


def write_structured_log(message: str, severity: str = "info", **fields):
    client = DatadogLogsClient()
    record = build_log_record(message, severity, event_type="structured", **fields)
    return client.write_log(record)
