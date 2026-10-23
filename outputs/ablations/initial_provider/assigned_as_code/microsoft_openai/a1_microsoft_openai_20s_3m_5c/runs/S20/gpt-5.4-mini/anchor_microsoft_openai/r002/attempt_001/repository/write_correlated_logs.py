import time

from observability_client import get_ingestion_client, load_observability_config
from observability_models import normalize_log_event


def write_correlated_logs(payload, config=None):
    settings = load_observability_config(config)
    client = get_ingestion_client(config)
    correlation_id = payload['correlation_id']
    timestamp_ms = payload.get('timestamp_ms', time.time() * 1000)
    logs = []
    for item in payload['events']:
        event = normalize_log_event(item, correlation_id=correlation_id)
        event['TimeGenerated'] = __import__('datetime').datetime.utcfromtimestamp(timestamp_ms / 1000).isoformat() + 'Z'
        logs.append(event)
    with client:
        client.upload(rule_id=settings.rule_id, stream_name=settings.stream_name, logs=logs)
    return {'submitted': True, 'correlation_id': correlation_id, 'count': len(logs)}
