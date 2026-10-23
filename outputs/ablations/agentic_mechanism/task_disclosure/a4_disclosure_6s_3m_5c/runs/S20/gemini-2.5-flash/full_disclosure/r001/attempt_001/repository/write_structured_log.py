from google.cloud import logging

def write_structured_log(log_name, message, severity="INFO", **kwargs):
    """Writes a structured JSON log event to Google Cloud Logging."""
    client = logging.Client()
    logger = client.logger(log_name)

    # Prepare the structured log entry
    log_entry = {
        "message": message,
        "severity": severity,
        **kwargs
    }

    logger.log_struct(log_entry)

if __name__ == "__main__":
    # Example usage:
    write_structured_log(
        log_name="my-application-logs",
        message="User login successful",
        severity="INFO",
        user_id="12345",
        ip_address="192.168.1.1"
    )
    print("Structured log written to Google Cloud Logging.")
