import os
import uuid
from datetime import datetime
from observability_client import ObservabilityClient
from observability_models import LogEntry

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
LOG_NAME = "my-structured-app-log"


def write_structured_log(
    message: str, service_name: str, user_id: str, latency_ms: int
):
    client = ObservabilityClient(project_id=PROJECT_ID)

    log_entry = LogEntry(
        severity="INFO",
        message=message,
        resource_type="global",
        resource_labels={"project_id": PROJECT_ID},
        json_payload={
            "serviceName": service_name,
            "userId": user_id,
            "latencyMs": latency_ms,
            "method": "GET",
            "path": "/api/v1/data",
        },
        labels={"environment": "production", "component": "api-gateway"},
    )

    client.write_log_entry(log_name=LOG_NAME, log_entry_data=log_entry)
    print(f"Wrote structured log to Google Cloud Logging: {message}")


if __name__ == "__main__":
    # Example usage:
    write_structured_log(
        message="Request processed successfully",
        service_name="data-service",
        user_id=str(uuid.uuid4()),
        latency_ms=120,
    )
