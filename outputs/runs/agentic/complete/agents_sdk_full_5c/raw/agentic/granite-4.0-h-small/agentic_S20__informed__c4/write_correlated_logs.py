import json
from observability_models import LogEvent
from observability_client import get_datadog_client

def write_correlated_logs(events: list[dict], request_id: str):
    """Write multiple structured log events that share the same request/correlation ID.

    events: a list of log event dicts with keys such as message, event_type, level
    request_id: shared correlation identifier to link the logs together
    """
    # Enrich each event with correlation info and common metadata
    enriched = [
        {
            'timestamp': int(os.getenv('SOURCE_TIMESTAMP', None)),
            'message': ev['message'],
            'event_type': ev['event_type'],
            'level': ev.get('level', 'info'),
            'request_id': request_id,
            'service': os.getenv('SERVICE_NAME', 'my_service'),
            'env': os.getenv('ENVIRONMENT', 'dev')
        }
        for ev in events
    ]
    client = get_datadog_client()
    response = client.logs.post(enriched)
    if response.ok:
        print('Correlated logs sent successfully.')
    else:
        print('Failed to send correlated logs:', response.text)
