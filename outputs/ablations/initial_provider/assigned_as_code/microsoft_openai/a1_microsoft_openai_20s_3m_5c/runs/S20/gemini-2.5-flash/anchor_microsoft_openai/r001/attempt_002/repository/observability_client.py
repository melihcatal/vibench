import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from azure.identity import DefaultAzureCredential
from azure.monitor.ingestion import LogsIngestionClient
from azure.monitor.query import LogsQueryClient, QueryTimeRange

from observability_models import LogEntry, QueryResults

class AzureMonitorClient:
    def __init__(self, workspace_id: Optional[str] = None, rule_id: Optional[str] = None, stream_name: Optional[str] = None, logging_endpoint: Optional[str] = None, query_endpoint: Optional[str] = None):
        self.workspace_id = workspace_id or os.getenv("AZURE_MONITOR_WORKSPACE_ID")
        self.rule_id = rule_id or os.getenv("AZURE_MONITOR_RULE_ID")
        self.stream_name = stream_name or os.getenv("AZURE_MONITOR_STREAM_NAME", "CustomLog")
        self.logging_endpoint = logging_endpoint or os.getenv("AZURE_MONITOR_LOGGING_ENDPOINT")
        self.query_endpoint = query_endpoint or os.getenv("AZURE_MONITOR_QUERY_ENDPOINT")

        if not all([self.workspace_id, self.rule_id, self.logging_endpoint, self.query_endpoint]):
            raise ValueError("Azure Monitor configuration missing. Ensure environment variables or constructor arguments are provided.")

    def ingest_log_entries(self, log_entries: List[LogEntry], table_name: str = "CustomLog") -> Dict[str, Any]:
        logs_to_upload = [entry.to_azure_monitor_format() for entry in log_entries]
        with DefaultAzureCredential() as credential:
            with LogsIngestionClient(endpoint=self.logging_endpoint, credential=credential) as client:
                client.upload(rule_id=self.rule_id, stream_name=self.stream_name, logs=logs_to_upload)
        return {"submitted": True, "count": len(log_entries)}

    def query_logs(self, kusto_query: str, time_range_start: datetime, time_range_end: datetime) -> QueryResults:
        with DefaultAzureCredential() as credential:
            client = LogsQueryClient(credential=credential)
            query_time_range = QueryTimeRange(
                start_time=time_range_start,
                end_time=time_range_end
            )
            response = client.query_workspace(
                workspace_id=self.workspace_id,
                query=kusto_query,
                timespan=query_time_range
            )
            
            logs = []
            if response.tables:
                for row in response.tables[0].rows:
                    log_data = {response.tables[0].columns[i].name: row[i] for i in range(len(row))}
                    message = log_data.get("message", "N/A")
                    severity = log_data.get("severity", "INFO")
                    timestamp_str = log_data.get("TimeGenerated")
                    timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00')) if timestamp_str else None
                    logs.append(LogEntry(message=message, severity=severity, timestamp=timestamp, **log_data))

            return QueryResults(logs=logs)
