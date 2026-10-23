from azure.identity import DefaultAzureCredential
from azure.monitor.ingestion import LogsIngestionClient
from azure.monitor.query import LogsQueryClient


def get_logs_client(config):
    credential = DefaultAzureCredential()
    return LogsIngestionClient(endpoint=config['endpoint'], credential=credential)


def get_query_client(config):
    credential = DefaultAzureCredential()
    return LogsQueryClient(credential)