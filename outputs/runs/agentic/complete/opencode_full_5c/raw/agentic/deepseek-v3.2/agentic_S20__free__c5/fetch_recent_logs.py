import os
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any
from observability_client import get_logging_client
from observability_models import LogQuery, LogEntry


def fetch_recent_logs(
    service_name: str,
    field_filters: Dict[str, str] = None,
    hours_back: int = 1,
    limit: int = 50,
) -> List[LogEntry]:
    """
    Retrieve recent log results from Azure Monitor Log Analytics filtered by field values and time range.

    Args:
        service_name: Name of the service/application
        field_filters: Dictionary of field=value pairs to filter logs
        hours_back: Number of hours to look back (default: 1)
        limit: Maximum number of log entries to return

    Returns:
        List of LogEntry objects containing filtered log data
    """
    try:
        from azure.identity import DefaultAzureCredential
        from azure.monitor.query import LogsQueryClient

        credential = DefaultAzureCredential()
        client = LogsQueryClient(credential)

        workspace_id = os.environ.get("AZURE_LOG_ANALYTICS_WORKSPACE_ID")
        if not workspace_id:
            raise ValueError(
                "AZURE_LOG_ANALYTICS_WORKSPACE_ID environment variable is required"
            )

        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=hours_back)

        filter_conditions = []
        if field_filters:
            for field, value in field_filters.items():
                filter_conditions.append(f'| where {field} contains "{value}"')

        filter_clause = "\n".join(filter_conditions)

        query = f"""
        AppRequests
        | where TimeGenerated between(datetime({start_time.strftime("%Y-%m-%d %H:%M:%S")}) .. datetime({end_time.strftime("%Y-%m-%d %H:%M:%S")}))
        | where AppRoleName contains "{service_name}"
        {filter_clause}
        | project TimeGenerated, AppRoleName, Message, SeverityLevel, OperationName, ClientIP, Success
        | order by TimeGenerated desc
        | take {limit}
        """

        response = client.query_workspace(
            workspace_id=workspace_id, query=query, timespan=timedelta(hours=hours_back)
        )

        log_entries = []

        for table in response.tables:
            for row in table.rows:
                entry_data = {}
                for i, col in enumerate(table.columns):
                    entry_data[col.name] = row[i]

                log_entry = LogEntry(
                    timestamp=entry_data.get("TimeGenerated", ""),
                    message=entry_data.get("Message", ""),
                    service=entry_data.get("AppRoleName", service_name),
                    level=entry_data.get("SeverityLevel", "INFO"),
                    operation=entry_data.get("OperationName", ""),
                    client_ip=entry_data.get("ClientIP", ""),
                    success=entry_data.get("Success", False),
                    raw_data=entry_data,
                )
                log_entries.append(log_entry)

        print(
            f"Fetched {len(log_entries)} recent logs from Azure Monitor for service: {service_name}"
        )
        return log_entries

    except Exception as e:
        print(f"Failed to fetch recent logs from Azure Monitor: {e}")

        try:
            from azure.core.exceptions import ClientAuthenticationError

            if isinstance(e, ClientAuthenticationError):
                print("Azure authentication failed. Check your Azure credentials.")
        except:
            pass

        return []
