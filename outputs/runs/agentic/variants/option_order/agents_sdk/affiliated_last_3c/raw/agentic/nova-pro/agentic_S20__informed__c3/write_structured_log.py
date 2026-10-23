import os
from azure.monitor.ingestion import LogsIngestionClient

client = LogsIngestionClient(endpoint=os.getenv('AZURE_MONITOR_LOGS_ENDPOINT'), credential=os.getenv('AZURE_MONITOR_LOGS_CREDENTIALS'))

def write_log(log_data):
    client.logs.write(log_data)