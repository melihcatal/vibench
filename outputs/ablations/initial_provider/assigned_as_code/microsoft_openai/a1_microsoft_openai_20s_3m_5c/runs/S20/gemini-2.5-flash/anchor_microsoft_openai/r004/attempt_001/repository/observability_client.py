import os
from azure.identity import DefaultAzureCredential
from azure.monitor.ingestion import LogsIngestionClient
from azure.monitor.query import LogsQueryClient
from azure.core.credentials import AzureKeyCredential

class ObservabilityClient:
    def __init__(self, config=None):
        self.config = config or {}
        self.credential = DefaultAzureCredential()
        self.log_ingestion_endpoint = self.config.get('LOG_INGESTION_ENDPOINT', os.environ.get('AZURE_LOG_INGESTION_ENDPOINT'))
        self.log_analytics_workspace_id = self.config.get('LOG_ANALYTICS_WORKSPACE_ID', os.environ.get('AZURE_LOG_ANALYTICS_WORKSPACE_ID'))
        self.log_analytics_shared_key = self.config.get('LOG_ANALYTICS_SHARED_KEY', os.environ.get('AZURE_LOG_ANALYTICS_SHARED_KEY')) # For query client with API key

    def get_logs_ingestion_client(self) -> LogsIngestionClient:
        if not self.log_ingestion_endpoint:
            raise ValueError("Log Ingestion Endpoint not configured.")
        return LogsIngestionClient(endpoint=self.log_ingestion_endpoint, credential=self.credential)

    def get_logs_query_client(self) -> LogsQueryClient:
        if not self.log_analytics_workspace_id:
            raise ValueError("Log Analytics Workspace ID not configured.")
        # Using DefaultAzureCredential for LogsQueryClient as well
        return LogsQueryClient(credential=self.credential)

    # Optionally, for specific scenarios where API key is preferred for query
    def get_logs_query_client_with_key(self) -> LogsQueryClient:
        if not self.log_analytics_workspace_id or not self.log_analytics_shared_key:
            raise ValueError("Log Analytics Workspace ID or Shared Key not configured.")
        return LogsQueryClient(credential=AzureKeyCredential(self.log_analytics_shared_key))
