from azure.identity import DefaultAzureCredential
from azure.monitor.query import LogsQueryClient
from datetime import datetime, timedelta


def write_correlated_logs(payloads, config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        client = LogsIngestionClient(endpoint=config['endpoint'], credential=credential)
        for payload in payloads:
            timestamp_ms = payload.get('timestamp_ms', time.time() * 1000)
            event = dict(payload['event'])
            event['TimeGenerated'] = datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc).isoformat()
            client.upload(rule_id=config['rule_id'], stream_name=config['stream_name'], logs=[event])
    return {'submitted': True}