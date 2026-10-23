import os
from observability_client import ObservabilityClient
from observability_models import LogEntry


def write_structured_log(
    severity: str, message: str, payload: dict, log_name: str = "application-logs"
):
    """Writes a structured JSON log event to Google Cloud Logging."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    client = ObservabilityClient(project_id, log_name=log_name)
    log_entry = LogEntry(severity=severity, message=message, json_payload=payload)
    client.write_log_entry(log_entry.to_dict())
    print(f"Structured log with severity '{severity}' written to Google Cloud Logging.")


if __name__ == "__main__":
    # Example usage:
    test_payload = {
        "event_type": "user_login",
        "user_id": "user-123",
        "ip_address": "192.168.1.1",
        "status": "success",
    }
    write_structured_log("INFO", "User login event", test_payload)
