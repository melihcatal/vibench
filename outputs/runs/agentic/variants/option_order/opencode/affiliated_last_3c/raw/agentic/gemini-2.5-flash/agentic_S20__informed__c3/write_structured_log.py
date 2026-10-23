from observability_client import ObservabilityClient
from observability_models import LogEntry


def write_structured_log(log_entry: LogEntry):
    client = ObservabilityClient()
    logger = client.get_logger()

    # Google Cloud Logging automatically handles structured logging if json_payload is provided
    logger.log_struct(
        log_entry.json_payload,
        severity=log_entry.severity,
        labels=log_entry.labels,
        # resource=logging.resource.Resource(type="global", labels={}), # Example if you need custom resource types
    )
    print(f"Structured log written with severity: {log_entry.severity}")


if __name__ == "__main__":
    # Example usage
    log_payload = {
        "event": "user_login",
        "user_id": "user-123",
        "ip_address": "192.168.1.1",
        "status": "success",
    }
    log_entry = LogEntry(
        message="User login event",
        severity="INFO",
        json_payload=log_payload,
        labels={"component": "auth", "env": "dev"},
    )
    write_structured_log(log_entry)
