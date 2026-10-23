from google.cloud import logging

def write_correlated_logs(log_name: str, correlation_id: str, messages: list[dict], severity: str = "INFO"):
    """
    Writes multiple structured JSON log events with a shared correlation identifier to Google Cloud Logging.

    Args:
        log_name: The name of the log to write to.
        correlation_id: A shared identifier to link related log entries.
        messages: A list of dictionaries, where each dictionary is a structured JSON payload.
        severity: The severity of the log entries.
    """
    client = logging.Client()
    logger = client.logger(log_name)

    for message in messages:
        # Add the correlation_id to each message's JSON payload
        message["correlation_id"] = correlation_id
        logger.log(json_payload=message, severity=severity)

if __name__ == "__main__":
    log_name = "my-correlated-app-logs"
    request_id = "req-7890"
    log_messages = [
        {
            "event_type": "request_start",
            "service": "api-gateway",
            "path": "/users",
            "method": "GET"
        },
        {
            "event_type": "database_query",
            "service": "user-service",
            "query": "SELECT * FROM users WHERE id = :id",
            "user_id": "user-abc"
        },
        {
            "event_type": "response_sent",
            "service": "api-gateway",
            "status_code": 200,
            "response_size": 1024
        }
    ]
    write_correlated_logs(log_name, request_id, log_messages, severity="INFO")
