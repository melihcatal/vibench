import os
import google.cloud.logging

def write_structured_log(log_name: str, message: str, severity: str = "INFO", component: str = "app-service"):
    """Writes a structured JSON log event to Google Cloud Logging."""
    client = google.cloud.logging.Client()
    logger = client.logger(log_name)

    # Structured log entry
    log_entry = {
        "message": message,
        "severity": severity,
        "component": component,
        "environment": os.getenv("APP_ENV", "development"),
    }
    logger.log_struct(log_entry, severity=severity)
    print(f"Logged structured message to {log_name} with severity {severity}")

if __name__ == "__main__":
    # Example usage:
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    write_structured_log("my-app-logs", "User login successful.", "INFO", "authentication")
    write_structured_log("my-app-logs", "Database connection error.", "ERROR", "database")
