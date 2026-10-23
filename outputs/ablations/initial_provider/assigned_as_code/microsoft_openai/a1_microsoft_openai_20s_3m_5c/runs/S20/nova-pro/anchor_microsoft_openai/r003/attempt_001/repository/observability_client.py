from datetime import datetime, timezone
from azure.identity import DefaultAzureCredential
from azure.monitor.ingestion import LogsIngestionClient
from azure.monitor.query import LogsQueryClient


def get_client(config=None):
    config = config or {}
    credential = DefaultAzureCredential()
    return LogsIngestionClient(endpoint=config['endpoint'], credential=credential), LogsQueryClient(credential)


def normalize_log_event(event):
    event['TimeGenerated'] = datetime.fromtimestamp(event['timestamp_ms'] / 1000, tz=timezone.utc).isoformat()
    return event