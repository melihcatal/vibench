import os
from azure.monitor.ingestion import LogsIngestionClient
from azure.monitor.query import LogsQueryClient

def get_ingestion_client():
    return LogsIngestionClient(endpoint=os.getenv('AZURE_MONITOR_LOGS_ENDPOINT'), credential=os.getenv('AZURE_MONITOR_LOGS_CREDENTIALS'))

def get_query_client():
    return LogsQueryClient(credential=os.getenv('AZURE_MONITOR_LOGS_CREDENTIALS'))