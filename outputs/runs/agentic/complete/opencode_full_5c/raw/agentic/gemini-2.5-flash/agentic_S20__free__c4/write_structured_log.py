import datetime
from typing import Dict, Any
from observability_client import ObservabilityClient


def write_structured_log(
    log_name: str,
    severity: str,
    message: str,
    json_payload: Dict[str, Any],
    resource_type: str = "global",
    resource_labels: Dict[str, str] = None,
    labels: Dict[str, str] = None,
):
    """Writes a structured JSON log event to Google Cloud Logging."""
    client = ObservabilityClient().logging_client

    entry = {
        "severity": severity.upper(),
        "jsonPayload": json_payload,
        "textPayload": message,
        "resource": {
            "type": resource_type,
            "labels": resource_labels
            if resource_labels is not None
            else {"project_id": client.project},
        },
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "labels": labels,
    }

    logger = client.logger(log_name)
    logger.log_struct(
        entry["jsonPayload"],
        severity=entry["severity"],
        text_payload=entry["textPayload"],
        resource=entry["resource"],
        labels=entry["labels"],
    )

    print(f"Wrote structured log to {log_name} with severity {severity}.")


if __name__ == "__main__":
    # Example usage
    LOG_NAME = "my-structured-app-log"
    PAYLOAD = {
        "event": "user_login",
        "user_id": "user-123",
        "ip_address": "192.168.1.1",
        "status": "success",
    }
    LABELS = {"environment": "development", "service": "auth-service"}
    write_structured_log(
        LOG_NAME, "INFO", "User logged in successfully", PAYLOAD, labels=LABELS
    )
