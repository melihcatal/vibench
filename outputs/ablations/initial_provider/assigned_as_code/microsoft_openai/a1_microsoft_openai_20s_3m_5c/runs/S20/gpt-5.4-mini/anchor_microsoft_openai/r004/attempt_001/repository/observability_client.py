import os
from dataclasses import dataclass

from azure.identity import DefaultAzureCredential
from azure.monitor.ingestion import LogsIngestionClient
from azure.monitor.query import LogsQueryClient


@dataclass
class ObservabilityConfig:
    endpoint: str
    rule_id: str = ""
    stream_name: str = ""


def load_observability_config(config=None):
    config = config or {}
    endpoint = config.get("endpoint") or os.environ["AZURE_MONITOR_DCE_ENDPOINT"]
    rule_id = config.get("rule_id") or os.environ.get("AZURE_MONITOR_DCR_RULE_ID", "")
    stream_name = config.get("stream_name") or os.environ.get("AZURE_MONITOR_STREAM_NAME", "")
    return ObservabilityConfig(endpoint=endpoint, rule_id=rule_id, stream_name=stream_name)


def build_credential():
    return DefaultAzureCredential()


def build_ingestion_client(config=None):
    obs_config = load_observability_config(config)
    credential = build_credential()
    return obs_config, credential, LogsIngestionClient(endpoint=obs_config.endpoint, credential=credential)


def build_query_client():
    return LogsQueryClient(credential=build_credential())
