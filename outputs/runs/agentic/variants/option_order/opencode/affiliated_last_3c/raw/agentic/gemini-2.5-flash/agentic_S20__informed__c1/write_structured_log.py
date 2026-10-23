import os
import json
from observability_client import get_logging_client
from observability_models import StructuredLogEntry


def write_structured_log(entry: StructuredLogEntry):
    client = get_logging_client()
    logger = client.logger(entry.log_name)

    # Google Cloud Logging automatically handles 'jsonPayload' when a dict is passed
    # It also handles 'severity' and 'resource' based on the LogEntry structure
    logger.log(
        json_payload=entry.json_payload,
        severity=entry.severity,
        resource={
            "type": entry.resource_type,
            "labels": entry.resource_labels,
        },
    )

    print(
        f"Structured log written to {entry.log_name}: {json.dumps(entry.json_payload)}"
    )


if __name__ == "__main__":
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
    else:
        log_entry = StructuredLogEntry(
            log_name="my-application-log",
            resource_type="global",
            resource_labels={
                "project_id": project_id,
            },
            json_payload={
                "event": "user_login",
                "user_id": "user-123",
                "ip_address": "192.168.1.1",
                "status": "success",
            },
            severity="INFO",
        )
        write_structured_log(log_entry)
