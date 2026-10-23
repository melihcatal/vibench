from datetime import datetime, timezone
import time
from azure.identity import DefaultAzureCredential
from azure.monitor.query import LogsQueryClient
from.observability_client import get_observability_client
from.observability_models import parse_log_response


def incident_summary(config=None):
    config = config or {}
    ingestion_client, query_client = get_observability_client(config)
    query = 'YourTableName | where Severity == "Error" and TimeGenerated > ago(1h)'
    options = LogsQueryOptions(start_time=datetime.now(timezone.utc) - timedelta(hours=1))
    response = query_client.query(query, options)
    logs = parse_log_response(response)
    summary = {
        'total_errors': len(logs),
        'earliest_error': min(logs, key=lambda x: x['TimeGenerated'])['TimeGenerated'] if logs else None,
        'latest_error': max(logs, key=lambda x: x['TimeGenerated'])['TimeGenerated'] if logs else None,
    }
    return summary

import timedelta