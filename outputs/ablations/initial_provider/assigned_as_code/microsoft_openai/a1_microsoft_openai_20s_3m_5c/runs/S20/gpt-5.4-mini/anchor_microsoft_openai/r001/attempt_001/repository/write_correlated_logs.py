from datetime import datetime, timezone
from azure.identity import DefaultAzureCredential
from azure.monitor.ingestion import LogsIngestionClient


def write_correlated_logs(payload, config=None):
    config = config or {}
    correlation_id = payload['correlation_id']
    timestamp = payload.get('timestamp_ms')
    events = []
    for event in payload['events']:
        item = dict(event)
        item['TimeGenerated'] = datetime.fromtimestamp((timestamp or item.get('timestamp_ms') or 0) / 1000, tz=timezone.utc).isoformat() if (timestamp or item.get('timestamp_ms')) else datetime.now(timezone.utc).isoformat()
        item['correlation_id'] = correlation_id
        events.append(item)
    with DefaultAzureCredential() as credential:
        with LogsIngestionClient(endpoint=config['endpoint'], credential=credential) as client:
            client.upload(rule_id=config['rule_id'], stream_name=config['stream_name'], logs=events)
    return {'submitted': True, 'count': len(events), 'correlation_id': correlation_id}
