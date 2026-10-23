
import os
import google.cloud.logging
import uuid

# Initialize Google Cloud Logging client
# Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
# or run on a Google Cloud platform that provides credentials automatically.
client = google.cloud.logging.Client()
logger = client.logger("my-application-logs")

def write_correlated_logs(request_id: str):
    """
    Writes application log events with a shared request or correlation identifier.
    """
    print(f"Writing logs for request_id: {request_id}")

    # Log an event at the start of a process
    logger.log_struct(
        {
            "message": "Processing started for request.",
            "correlation_id": request_id,
            "event_type": "PROCESS_START",
        },
        severity="INFO",
    )

    # Simulate some work
    import time
    time.sleep(0.1)

    # Log an event during the process
    logger.log_struct(
        {
            "message": "Performing a sub-task.",
            "correlation_id": request_id,
            "event_type": "SUB_TASK",
            "task_name": "data_validation",
        },
        severity="DEBUG",
    )

    time.sleep(0.1)

    # Log an event at the end of a process
    logger.log_struct(
        {
            "message": "Processing completed for request.",
            "correlation_id": request_id,
            "event_type": "PROCESS_END",
            "status": "SUCCESS",
        },
        severity="INFO",
    )
    print(f"Finished writing logs for request_id: {request_id}")

if __name__ == "__main__":
    # Example usage: Generate a unique request ID for a series of correlated logs
    new_request_id = str(uuid.uuid4())
    write_correlated_logs(new_request_id)

    another_request_id = str(uuid.uuid4())
    write_correlated_logs(another_request_id)
