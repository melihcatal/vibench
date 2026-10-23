from google.cloud import logging

def write_structured_log(project_id: str, log_id: str, message: dict):
    """Writes a structured JSON log event to Google Cloud Logging."""
    client = logging.Client(project=project_id)
    logger = client.logger(log_id)
    logger.log_struct(message)

if __name__ == "__main__":
    # Replace with your Google Cloud Project ID and desired log ID
    PROJECT_ID = "your-gcp-project-id" 
    LOG_ID = "my-structured-log"

    # Example structured log message
    log_payload = {
        "event": "user_action",
        "user": "test_user",
        "action": "login",
        "timestamp": "2026-09-19T10:00:00Z",
        "details": {
            "ip_address": "192.168.1.1",
            "device": "desktop"
        }
    }

    print(f"Writing structured log to Google Cloud Logging (Project: {PROJECT_ID}, Log: {LOG_ID})...")
    write_structured_log(PROJECT_ID, LOG_ID, log_payload)
    print("Log event written successfully.")
