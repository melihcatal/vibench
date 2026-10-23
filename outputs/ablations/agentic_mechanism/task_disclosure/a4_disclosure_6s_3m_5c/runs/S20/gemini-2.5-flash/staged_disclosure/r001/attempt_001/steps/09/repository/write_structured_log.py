import google.cloud.logging
import os

def write_structured_log():
    # Instantiates a client
    client = google.cloud.logging.Client()

    # The name of the log to write to
    log_name = "my-structured-log"

    # Selects the log to write to
    logger = client.logger(log_name)

    # Structured log entry
    log_entry = {
        "message": "This is a structured log entry.",
        "severity": "INFO",
        "resource": {
            "type": "global",
            "labels": {
                "project_id": os.environ.get("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
            }
        },
        "jsonPayload": {
            "event_type": "user_action",
            "user_id": "user-123",
            "action": "login",
            "timestamp": "2026-09-19T10:00:00Z"
        }
    }

    # Writes the structured log entry
    logger.log_struct(
        log_entry["jsonPayload"],
        severity=log_entry["severity"],
        resource=log_entry["resource"]
    )

    print(f"Structured log written to Google Cloud Logging log: {log_name}")

if __name__ == "__main__":
    write_structured_log()
