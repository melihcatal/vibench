from google.cloud import logging
import os
import json

def write_correlated_log(log_name, message, correlation_id, severity="INFO", project_id=None):
    """Writes a structured log entry with a correlation ID to Google Cloud Logging.

    Args:
        log_name (str): The name of the log to write to.
        message (str): The main log message.
        correlation_id (str): The shared request or correlation identifier.
        severity (str): The severity of the log entry (e.g., "INFO", "ERROR").
        project_id (str, optional): Your Google Cloud project ID. If not provided,
                                     it will try to get it from the GOOGLE_CLOUD_PROJECT environment variable.
    """
    if project_id is None:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            raise ValueError("Google Cloud Project ID not provided and GOOGLE_CLOUD_PROJECT environment variable not set.")

    client = logging.Client(project=project_id)
    logger = client.logger(log_name)

    # Structured log entry
    log_entry = {
        "message": message,
        "correlation_id": correlation_id,
        "severity": severity,
        "component": "application-logs"
    }

    # Write the log entry
    logger.log_struct(
        log_entry,
        severity=severity
    )

if __name__ == "__main__":
    # Example usage:
    # Set your Google Cloud Project ID either as an environment variable or pass it directly
    # os.environ["GOOGLE_CLOUD_PROJECT"] = "your-gcp-project-id"

    # For demonstration, use a placeholder project ID if not set
    # In a real application, ensure GOOGLE_CLOUD_PROJECT is set or passed.
    example_project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id-here")

    try:
        write_correlated_log(
            log_name="my-app-logs",
            message="User login initiated.",
            correlation_id="req-12345",
            severity="INFO",
            project_id=example_project_id
        )
        write_correlated_log(
            log_name="my-app-logs",
            message="Processing user request data.",
            correlation_id="req-12345",
            severity="DEBUG",
            project_id=example_project_id
        )
        write_correlated_log(
            log_name="my-app-logs",
            message="Error fetching data for user.",
            correlation_id="req-12345",
            severity="ERROR",
            project_id=example_project_id
        )
        print("Correlated log entries written successfully.")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

