from datetime import datetime, timezone
import time
from azure.identity import DefaultAzureCredential
from azure.monitor.query import LogsQueryClient, LogsQueryOptions


def fetch_recent_logs(config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        client = LogsQueryClient(credential)
        query = 'YourTableName | where TimeGenerated > ago(1h)'
        options = LogsQueryOptions(start_time=datetime.now(timezone.utc) - timedelta(hours=1))
        response = client.query(query, options)
        return response.tables[0].rows if response.tables else []

import timedelta