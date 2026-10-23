from observability_client import get_logging_client
from observability_models import create_log_entry
import uuid


def write_correlated_logs(log_name, correlation_id, log_events):
    """
    Writes multiple application log events that include a shared request or correlation identifier.
    """
    client = get_logging_client()
    logger = client.logger(log_name)

    for event in log_events:
        severity = event.get("severity", "INFO")
        message = event.get("message", "")
        json_payload = event.get("json_payload", {})

        entry = create_log_entry(
            severity, message, json_payload=json_payload, correlation_id=correlation_id
        )
        logger.log_struct(entry["jsonPayload"], severity=entry["severity"])


if __name__ == "__main__":
    # Example usage:
    # correlation_id = str(uuid.uuid4())
    # log_events = [
    #     {"severity": "INFO", "message": "Request started", "json_payload": {"path": "/api/data"}},
    #     {"severity": "DEBUG", "message": "Processing data", "json_payload": {"step": 1}},
    #     {"severity": "INFO", "message": "Request completed", "json_payload": {"status": 200}},
    # ]
    # write_correlated_logs("my-app-logs", correlation_id, log_events)
    pass
