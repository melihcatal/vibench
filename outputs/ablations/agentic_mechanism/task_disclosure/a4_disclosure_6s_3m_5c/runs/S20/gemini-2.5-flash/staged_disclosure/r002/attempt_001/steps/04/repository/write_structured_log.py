from google.cloud import logging

def write_structured_log(log_name, message, severity="INFO"):
    """Writes a structured JSON log event to Google Cloud Logging.

    Args:
        log_name (str): The name of the log to write to (e.g., "my-application-log").
        message (dict): A dictionary representing the structured log message.
        severity (str): The severity level of the log (e.g., "INFO", "ERROR", "DEBUG").
    """
    client = logging.Client()
    logger = client.logger(log_name)

    logger.log_struct(
        message,
        severity=severity
    )

if __name__ == "__main__":
    # Example usage:
    log_name = "my-application-log"
    structured_message = {
        "event_type": "user_login",
        "user_id": "user123",
        "ip_address": "192.168.1.1",
        "status": "success"
    }
    write_structured_log(log_name, structured_message, severity="INFO")
    print(f"Structured log written to Google Cloud Logging under log '{log_name}'")
