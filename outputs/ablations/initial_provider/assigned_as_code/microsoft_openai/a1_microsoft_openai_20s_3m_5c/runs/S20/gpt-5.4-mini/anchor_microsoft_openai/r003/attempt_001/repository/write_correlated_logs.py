from datetime import datetime, timezone

from azure.identity import DefaultAzureCredential
from azure.monitor.ingestion import LogsIngestionClient


def write_correlated_logs(payload, config=None):
    config = config or {}
    correlation_id = payload['correlation_id']
    base_time = payload.get('timestamp_ms')
    events = []
    for item in payload['events']:
        event = dict(item)
        event['correlation_id'] = correlation_id
        if base_time is not None and 'timestamp_ms' not in event:
            event['timestamp_ms'] = base_time
        timestamp_ms = event.get('timestamp_ms')
        if timestamp_ms is not None:
            event['TimeGenerated'] = datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc).isoformat()
        events.append(event)
    with DefaultAzureCredential() as credential:
        with LogsIngestionClient(endpoint=config['endpoint'], credential=credential) as client:
            client.upload(rule_id=config['rule_id'], stream_name=config['stream_name'], logs=events)
    return {'submitted': True, 'correlation_id': correlation_id, 'count': len(events)}
