from azure.identity import DefaultAzureCredential
from azure.monitor.ingestion import LogsIngestionClient
from azure.monitor.query import LogsQueryClient


def get_observability_client(config):
    credential = DefaultAzureCredential()
    ingestion_client = LogsIngestionClient(endpoint=config['endpoint'], credential=credential)
    query_client = LogsQueryClient(credential)
    return ingestion_client, query_client