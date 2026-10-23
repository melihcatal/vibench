from google.cloud import logging
import os
import json

def write_structured_log(log_name: str, message: dict):
    """Writes a structured JSON log event to Google Cloud Logging."""
    client = logging.Client()
    logger = client.logger(log_name)

    # Example of adding a severity, which is a common field in structured logs
    message['severity'] = message.get('severity', 'INFO')

    logger.log_struct(message)
    print(f"Structured log written to {log_name}: {json.dumps(message)}")

if __name__ == '__main__':
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        print("GOOGLE_CLOUD_PROJECT environment variable not set.")
        exit(1)
    
    log_name = "my-application-logs" # Replace with your log name

    example_log_entry = {
        "event_type": "user_login",
        "user_id": "user-123",
        "ip_address": "192.168.1.1",
        "status": "success",
        "latency_ms": 50,
        "message": "User logged in successfully."
    }
    write_structured_log(log_name, example_log_entry)
