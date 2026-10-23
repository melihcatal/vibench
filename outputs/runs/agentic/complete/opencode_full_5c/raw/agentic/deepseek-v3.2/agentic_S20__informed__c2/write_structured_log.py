import os
import json
from datetime import datetime
from typing import Dict, Any, Optional
from google.cloud import logging
from observability_models import StructuredLogPayload


def write_structured_log(
    message: str,
    severity: str = "INFO",
    component: Optional[str] = None,
    user_id: Optional[str] = None,
    request_id: Optional[str] = None,
    additional_fields: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Write a structured JSON log event to Google Cloud Logging.

    Args:
        message: The log message
        severity: Log severity (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        component: Application component name
        user_id: User identifier
        request_id: Request correlation ID
        additional_fields: Additional structured fields
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set")

    client = logging.Client(project=project_id)
    logger = client.logger("structured-logs")

    payload = StructuredLogPayload(
        message=message,
        severity=severity,
        component=component,
        user_id=user_id,
        request_id=request_id,
        additional_fields=additional_fields,
    )

    log_data = payload.to_dict()
    log_data["timestamp"] = datetime.utcnow().isoformat()

    logger.log_struct(log_data, severity=severity)

    print(f"Structured log written to Google Cloud Logging with severity: {severity}")


if __name__ == "__main__":
    write_structured_log(
        message="User authentication successful",
        severity="INFO",
        component="auth-service",
        user_id="user-12345",
        request_id="req-67890",
        additional_fields={"auth_method": "oauth2", "duration_ms": 150},
    )
