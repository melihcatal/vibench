import datetime
from observability_client import ObservabilityClient
from observability_models import LogEntry


def write_structured_log(
    log_name: str, message: str, severity: str, json_payload: dict
):
    client = ObservabilityClient()
    logger = client.get_logger(log_name)

    log_entry = LogEntry(
        message=message,
        severity=severity,
        timestamp=datetime.datetime.now(datetime.timezone.utc),
        json_payload=json_payload,
        resource={"type": "global", "labels": {"project_id": client.project_id}},
    )

    logger.log_struct(log_entry.json_payload, severity=log_entry.severity)

    return {
        "status": "success",
        "log_name": log_name,
        "severity": severity,
        "message": message,
    }
