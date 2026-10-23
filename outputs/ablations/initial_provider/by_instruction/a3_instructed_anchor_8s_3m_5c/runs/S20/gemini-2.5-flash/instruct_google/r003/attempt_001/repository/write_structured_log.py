from observability_client import ObservabilityClient
from observability_models import StructuredLogEntry

def write_structured_log(log_name: str, entry: StructuredLogEntry):
    client = ObservabilityClient()
    logger = client.get_logger(log_name)

    # Google Cloud Logging expects json_payload as a dict directly
    # and other fields like severity, resource, labels as separate arguments
    logger.log(
        text_payload=entry.message, # Use text_payload for the main message if json_payload is also present
        severity=entry.severity,
        resource=entry.resource,
        labels=entry.labels,
        json_payload=entry.json_payload # Structured data goes here
    )


if __name__ == "__main__":
    # Example Usage:
    log_entry = StructuredLogEntry(
        message="This is a test structured log entry.",
        severity="INFO",
        resource={
            "type": "global",
            "labels": {
                "project_id": "your-gcp-project-id" # Replace with your GCP Project ID
            },
        },
        labels={
            "environment": "development",
            "service": "my-app"
        },
        json_payload={
            "event_type": "user_action",
            "user_id": "12345",
            "action": "login",
            "details": {"ip_address": "192.168.1.1", "device": "mobile"}
        }
    )
    write_structured_log("my-application-logs", log_entry)
