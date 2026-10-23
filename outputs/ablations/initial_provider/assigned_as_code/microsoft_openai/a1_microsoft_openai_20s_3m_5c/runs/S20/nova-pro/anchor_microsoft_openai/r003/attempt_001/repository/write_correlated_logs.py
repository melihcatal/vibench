from datetime import datetime, timezone
import time
from azure.identity import DefaultAzureCredential
from azure.monitor.ingestion import LogsIngestionClient


def write_correlated_logs(payloads, config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        with LogsIngestionClient(endpoint=config['endpoint'], credential=credential) as client:
            for payload in payloads:
                timestamp_ms = payload.get('timestamp_ms', time.time() * 1000)
                event = dict(payload['event'])
                event['TimeGenerated'] = datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc).isoformat()
                client.upload(rule_id=config['rule_id'], stream_name=config['stream_name'], logs=[event])
    return {'submitted': True}