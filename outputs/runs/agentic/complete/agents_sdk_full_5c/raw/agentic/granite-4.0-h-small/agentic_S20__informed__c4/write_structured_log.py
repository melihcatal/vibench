import json
from observability_models import LogEvent
from observability_client import get_datadog_client

def write_structured_log(event_type: str, message: str, request_id: str):
    """Write a structured JSON log event to Datadog Logs using the Datadog SDK/client.

    event_type: a short identifier for the log (e.g., 'request_start')
    message: the log message text
    request_id: a correlation ID to tie related logs together
    """
    log_event = {
        'timestamp': int(os.getenv('SOURCE_TIMESTAMP', None)),
        'message': message,
        'event_type': event_type,
        'request_id': request_id,
        'service': os.getenv('SERVICE_NAME', 'my_service'),
        'env': os.getenv('ENVIRONMENT', 'dev'),
        'level': 'info'
    }
    client = get_datadog_client()
    # Use the Logs API endpoint to send a JSON payload
    response = client.logs.post([log_event])
    if response.ok:
        print('Log successfully sent to Datadog.')
    else:
        print('Failed to send log:', response.text)
