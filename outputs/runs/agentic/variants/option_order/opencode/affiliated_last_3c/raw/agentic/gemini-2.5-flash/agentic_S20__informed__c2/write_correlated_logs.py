import os
from observability_client import ObservabilityClient
from observability_models import LogEntry


def write_correlated_logs(
    correlation_id: str, events: list[dict], log_name: str = "application-logs"
):
    """Writes application log events with a shared correlation identifier to Google Cloud Logging."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    client = ObservabilityClient(project_id, log_name=log_name)

    for event in events:
        severity = event.get("severity", "INFO")
        message = event.get("message", "")
        payload = event.get("json_payload", {})
        payload["correlation_id"] = correlation_id  # Add correlation ID to payload

        log_entry = LogEntry(severity=severity, message=message, json_payload=payload)
        client.write_log_entry(log_entry.to_dict())
        print(
            f"Correlated log for ID '{correlation_id}' with severity '{severity}' written."
        )


if __name__ == "__main__":
    # Example usage:
    request_id = "req-abc-123"
    log_events = [
        {
            "severity": "INFO",
            "message": "Request received",
            "json_payload": {"path": "/api/data"},
        },
        {
            "severity": "DEBUG",
            "message": "Processing data",
            "json_payload": {"step": 1, "data_size": 1024},
        },
        {
            "severity": "INFO",
            "message": "Request completed",
            "json_payload": {"status_code": 200},
        },
    ]
    write_correlated_logs(request_id, log_events)
