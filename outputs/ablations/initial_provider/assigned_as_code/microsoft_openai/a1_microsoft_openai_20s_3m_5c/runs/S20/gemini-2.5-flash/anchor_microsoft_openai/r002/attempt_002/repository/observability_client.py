import os
from azure.identity import DefaultAzureCredential
from azure.monitor.ingestion import LogsIngestionClient
from azure.monitor.query import LogsQueryClient

def get_ingestion_client():
    endpoint = os.environ.get("AZURE_LOG_INGESTION_ENDPOINT")
    rule_id = os.environ.get("AZURE_LOG_INGESTION_RULE_ID")
    stream_name = os.environ.get("AZURE_LOG_INGESTION_STREAM_NAME")

    if not all([endpoint, rule_id, stream_name]):
        raise ValueError("Missing Azure Monitor Ingestion environment variables: AZURE_LOG_INGESTION_ENDPOINT, AZURE_LOG_INGESTION_RULE_ID, AZURE_LOG_INGESTION_STREAM_NAME")

    credential = DefaultAzureCredential()
    client = LogsIngestionClient(endpoint=endpoint, credential=credential)
    return client, rule_id, stream_name

def get_query_client():
    credential = DefaultAzureCredential()
    client = LogsQueryClient(credential=credential)
    return client
