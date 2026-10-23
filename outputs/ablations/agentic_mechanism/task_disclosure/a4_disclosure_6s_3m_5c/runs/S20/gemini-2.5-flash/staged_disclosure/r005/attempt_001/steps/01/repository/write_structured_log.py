from google.cloud import logging

def write_structured_log(log_name: str, message: str, severity: str = "INFO", **kwargs):
    """Writes a structured log event to Google Cloud Logging.

    Args:
        log_name: The name of the log to write to.
        message: The main message for the log entry.
        severity: The severity of the log entry (e.g., "DEBUG", "INFO", "WARNING", "ERROR").
        **kwargs: Additional fields to include in the structured log entry.
    """
    client = logging.Client()
    logger = client.logger(log_name)

    # Create a structured log entry
    log_entry = {
        "message": message,
        "severity": severity,
        **kwargs,
    }

    logger.log_struct(
        log_entry,
        severity=severity,
    )

if __name__ == "__main__":
    # Example usage:
    # To run this example, you need to have Google Cloud credentials configured.
    # For more information, see: https://cloud.google.com/docs/authentication/getting-started
    
    # You can specify a custom log name
    my_log_name = "my-application-log" 

    print(f"Writing a structured log to Google Cloud Logging under log name: {my_log_name}")
    write_structured_log(
        log_name=my_log_name,
        message="This is a structured log event.",
        severity="INFO",
        event_type="user_action",
        user_id="12345",
        transaction_id="abc-123",
    )
    print("Structured log written successfully.")
