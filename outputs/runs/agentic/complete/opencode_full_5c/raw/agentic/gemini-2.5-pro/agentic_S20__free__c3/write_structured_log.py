from google.cloud import logging
from google.cloud.logging.resource import Resource
import os
import datetime
import uuid


def write_structured_log():
    """Writes a structured log entry to Google Cloud Logging."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set.")

    client = logging.Client(project=project_id)

    log_name = "structured-log-test"
    logger = client.logger(log_name)

    # Define a resource for the log.
    # This could be a GKE container, a GCE instance, or a global resource.
    res = Resource(
        type="global",
        labels={},
    )

    request_id = str(uuid.uuid4())
    user_id = "user_12345"

    # The structured payload (JSON)
    json_payload = {
        "event_time": datetime.datetime.utcnow().isoformat() + "Z",
        "message": "User action logged.",
        "request_id": request_id,
        "user": {"id": user_id, "ip_address": "192.0.2.1"},
        "http_request": {
            "request_method": "POST",
            "request_url": "/api/v1/items",
            "status": 201,
            "user_agent": "My-App/1.0",
        },
    }

    logger.log_json(json_payload, resource=res, severity="INFO")


if __name__ == "__main__":
    write_structured_log()
