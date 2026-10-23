import datetime
import uuid
from observability_client import ObservabilityClient
from observability_models import LogEntry


def write_correlated_logs(
    log_name: str, messages: list[str], severity: str, correlation_id: str | None = None
):
    client = ObservabilityClient()
    logger = client.get_logger(log_name)

    if correlation_id is None:
        correlation_id = str(uuid.uuid4())

    results = []
    for message in messages:
        log_entry = LogEntry(
            message=message,
            severity=severity,
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            labels={"correlation_id": correlation_id},
            resource={"type": "global", "labels": {"project_id": client.project_id}},
        )

        # For correlated logs, it's common to include the correlation_id in the payload or labels
        # Google Cloud Logging can correlate logs using `trace` field, but for simple correlation_id in payload/labels works well too.
        # If using OpenTelemetry or similar, `trace` context would be propagated automatically.
        entry_payload = {"message": log_entry.message, "correlation_id": correlation_id}
        logger.log_struct(
            entry_payload, severity=log_entry.severity, labels=log_entry.labels
        )
        results.append(
            {
                "status": "success",
                "log_name": log_name,
                "severity": severity,
                "message": message,
                "correlation_id": correlation_id,
            }
        )

    return results
