from datetime import datetime, timezone
import time
from azure.identity import DefaultAzureCredential
from azure.monitor.ingestion import LogsIngestionClient

from observability_client import get_logs_client


def write_correlated_logs(payloads, correlation_id, config=None):
    config = config or {}
    client = get_logs_client(config)
    logs = []
    for payload in payloads:
        timestamp_ms = payload.get('timestamp_ms', time.time() * 1000)
        event = dict(payload['event'])
        event['TimeGenerated'] = datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc).isoformat()
        event['CorrelationId'] = correlation_id
        logs.append(event)
    client.upload(rule_id=config['rule_id'], stream_name=config['stream_name'], logs=logs)
    return {'submitted': True}