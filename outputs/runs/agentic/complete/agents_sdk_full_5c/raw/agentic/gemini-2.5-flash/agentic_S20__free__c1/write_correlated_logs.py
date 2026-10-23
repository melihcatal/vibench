from google.cloud import logging
import os
import json
import uuid

def write_correlated_logs(log_name: str, correlation_id: str, messages: list[dict]):
    """Writes application log events with a shared correlation identifier to Google Cloud Logging."""
    client = logging.Client()
    logger = client.logger(log_name)

    for message_data in messages:
        # Ensure correlation_id is part of the structured log payload
        message_data["correlation_id"] = correlation_id
        message_data['severity'] = message_data.get('severity', 'INFO')
        logger.log_struct(message_data)
        print(f"Correlated log written to {log_name} with correlation_id {correlation_id}: {json.dumps(message_data)}")

if __name__ == '__main__':
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        print("GOOGLE_CLOUD_PROJECT environment variable not set.")
        exit(1)

    log_name = "my-application-logs" # Replace with your log name
    
    # Generate a unique correlation ID for a simulated request
    current_correlation_id = str(uuid.uuid4())

    example_log_events = [
        {"event_type": "request_start", "path": "/api/data", "method": "GET", "message": "Request processing started."},
        {"event_type": "db_query", "table": "users", "query_time_ms": 150, "message": "Database query executed."},
        {"event_type": "request_end", "status_code": 200, "message": "Request processing finished successfully."}
    ]
    write_correlated_logs(log_name, current_correlation_id, example_log_events)
