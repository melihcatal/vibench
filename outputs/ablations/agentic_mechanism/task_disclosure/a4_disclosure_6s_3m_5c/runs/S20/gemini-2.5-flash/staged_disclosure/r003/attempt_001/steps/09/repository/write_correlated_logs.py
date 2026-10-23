import google.cloud.logging
import uuid
import datetime

# Instantiates a client
client = google.cloud.logging.Client()

# The name of the log to write to
log_name = "application_logs"
logger = client.logger(log_name)

def write_correlated_logs(request_id):
    """
    Writes application log events with a shared request or correlation identifier.
    """
    
    # Log an info entry
    logger.log_struct(
        {
            "message": "User login initiated",
            "user_id": "user-123",
            "event_type": "login_attempt",
            "correlation_id": request_id
        },
        severity="INFO"
    )

    # Log another info entry for the same request
    logger.log_struct(
        {
            "message": "Fetching user profile",
            "user_id": "user-123",
            "event_type": "fetch_profile",
            "correlation_id": request_id
        },
        severity="INFO"
    )

    # Log a debug entry for the same request
    logger.log_struct(
        {
            "message": "Database query executed",
            "query": "SELECT * FROM users WHERE id = 'user-123'",
            "correlation_id": request_id
        },
        severity="DEBUG"
    )

if __name__ == "__main__":
    correlation_id = str(uuid.uuid4())
    print(f"Writing logs with correlation ID: {correlation_id}")
    write_correlated_logs(correlation_id)
    print("Logs written. Please check Google Cloud Logging.")
