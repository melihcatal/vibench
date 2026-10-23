import os
import json
from datetime import datetime, timezone, timedelta
from azure.identity import DefaultAzureCredential
from azure.monitor.ingestion import LogsIngestionClient
from azure.monitor.query import LogsQueryClient, QueryTimeframe
from observability_models import LogEntry, StructuredLogEntry, CorrelatedLogEntry

class ObservabilityClient:
    def __init__(self, 
                 ingestion_endpoint: str = os.environ.get("AZURE_LOG_INGESTION_ENDPOINT"),
                 workspace_id: str = os.environ.get("AZURE_LOG_WORKSPACE_ID"),
                 rule_id: str = os.environ.get("AZURE_LOG_RULE_ID"),
                 stream_name: str = os.environ.get("AZURE_LOG_STREAM_NAME")):

        if not all([ingestion_endpoint, workspace_id, rule_id, stream_name]):
            raise ValueError("Missing one or more Azure Monitor configuration environment variables.")

        self.ingestion_endpoint = ingestion_endpoint
        self.workspace_id = workspace_id
        self.rule_id = rule_id
        self.stream_name = stream_name
        self.credential = DefaultAzureCredential()
        self.ingestion_client = LogsIngestionClient(endpoint=self.ingestion_endpoint, credential=self.credential)
        self.query_client = LogsQueryClient(credential=self.credential)

    def ingest_log(self, log_entry: LogEntry, custom_table_name: str = "MyPythonLogs") -> dict:
        log_data = {
            "TimeGenerated": datetime.fromisoformat(log_entry.timestamp).isoformat(),
            "Severity": log_entry.severity,
            "Message": log_entry.message,
            "ResourceId": log_entry.resource_id,
        }
        if log_entry.properties:
            log_data.update(log_entry.properties)

        if isinstance(log_entry, CorrelatedLogEntry):
            log_data["CorrelationId"] = log_entry.correlation_id
        
        # Azure Monitor Ingestion client expects a list of dictionaries
        # The custom_table_name is not directly used in the upload method but is a logical construct 
        # for how logs might be organized in Azure Monitor. For the actual ingestion, 
        # the stream_name (data collection stream) and rule_id (data collection rule) are used.
        self.ingestion_client.upload(rule_id=self.rule_id, stream_name=self.stream_name, logs=[log_data])
        return {"submitted": True}

    def query_logs(self, query: str, duration_hours: int = 1) -> list[dict]:
        # Define the time range for the query
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(hours=duration_hours)
        query_timeframe = QueryTimeframe(start_time=start_time, end_time=end_time)

        response = self.query_client.query_workspace(
            workspace_id=self.workspace_id,
            query=query,
            timespan=query_timeframe
        )

        results = []
        for table in response.tables:
            for row in table.rows:
                results.append(dict(zip(table.columns, row)))
        return results
