from observability_client import get_logging_client
from observability_models import create_log_entry


def write_structured_log(log_name, severity, message, json_payload):
    """
    Writes a structured JSON log event to Google Cloud Logging.
    """
    client = get_logging_client()
    logger = client.logger(log_name)

    entry = create_log_entry(severity, message, json_payload=json_payload)
    logger.log_struct(entry["jsonPayload"], severity=entry["severity"])


if __name__ == "__main__":
    # Example usage:
    # write_structured_log("my-app-logs", "INFO", "User login event", {"user_id": "123", "ip_address": "192.168.1.1"})
    pass
