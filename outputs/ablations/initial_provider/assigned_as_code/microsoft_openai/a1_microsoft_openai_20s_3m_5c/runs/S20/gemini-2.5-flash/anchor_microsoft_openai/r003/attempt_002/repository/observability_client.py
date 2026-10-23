from azure.identity import DefaultAzureCredential
from azure.monitor.ingestion import LogsIngestionClient
from azure.monitor.query import LogsQueryClient

class ObservabilityClient:
    def __init__(self, ingestion_endpoint: str, query_endpoint: str = None):
        self.credential = DefaultAzureCredential()
        self.ingestion_client = LogsIngestionClient(endpoint=ingestion_endpoint, credential=self.credential)
        if query_endpoint:
            self.query_client = LogsQueryClient(credential=self.credential)
        else:
            self.query_client = None

    def get_ingestion_client(self) -> LogsIngestionClient:
        return self.ingestion_client

    def get_query_client(self) -> LogsQueryClient:
        if not self.query_client:
            raise ValueError("Query client not initialized. Provide a query_endpoint during client creation.")
        return self.query_client
