import time
import uuid
from observability_client import get_ingestion_client
from observability_models import LogEvent

def write_correlated_logs(messages: list[str], correlation_id: str | None = None, severity: str = "Informational"):
    if correlation_id is None:
        correlation_id = str(uuid.uuid4())

    client, rule_id, stream_name = get_ingestion_client()

    logs_to_upload = []
    for message in messages:
        event_payload = {
            "Message": message,
            "CorrelationId": correlation_id,
        }
        log_event = LogEvent(
            message=message,
            severity=severity,
            timestamp_ms=int(time.time() * 1000),
            properties=event_payload
        )
        logs_to_upload.append(log_event.to_azure_monitor_log())

    client.upload(rule_id=rule_id, stream_name=stream_name, logs=logs_to_upload)
    return {"submitted": True, "correlation_id": correlation_id}
