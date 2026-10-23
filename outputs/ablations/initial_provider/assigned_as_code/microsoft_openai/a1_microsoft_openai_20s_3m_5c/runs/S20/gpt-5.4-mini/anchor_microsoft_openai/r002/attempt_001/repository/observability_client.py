import os
from dataclasses import dataclass

from azure.identity import DefaultAzureCredential
from azure.monitor.ingestion import LogsIngestionClient
from azure.monitor.query import LogsQueryClient


@dataclass
class ObservabilityConfig:
    endpoint: str
    workspace_id: str | None = None
    rule_id: str | None = None
    stream_name: str | None = None


def load_observability_config(config=None):
    config = config or {}
    return ObservabilityConfig(
        endpoint=config.get('endpoint') or os.environ['AZURE_MONITOR_LOGS_INGESTION_ENDPOINT'],
        workspace_id=config.get('workspace_id') or os.environ.get('AZURE_MONITOR_WORKSPACE_ID'),
        rule_id=config.get('rule_id') or os.environ.get('AZURE_MONITOR_DCR_RULE_ID'),
        stream_name=config.get('stream_name') or os.environ.get('AZURE_MONITOR_DCR_STREAM_NAME'),
    )


def get_credential():
    return DefaultAzureCredential()


def get_ingestion_client(config=None):
    settings = load_observability_config(config)
    return LogsIngestionClient(endpoint=settings.endpoint, credential=get_credential())


def get_query_client():
    return LogsQueryClient(credential=get_credential())
