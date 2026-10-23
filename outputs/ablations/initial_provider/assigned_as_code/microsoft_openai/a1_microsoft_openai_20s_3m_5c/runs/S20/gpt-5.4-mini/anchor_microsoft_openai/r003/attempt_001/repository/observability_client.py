import os
from datetime import datetime, timezone

from azure.identity import DefaultAzureCredential
from azure.monitor.query import LogsQueryClient


def load_observability_config(config=None):
    config = dict(config or {})
    config.setdefault('workspace_id', os.environ.get('AZURE_LOG_ANALYTICS_WORKSPACE_ID'))
    config.setdefault('endpoint', os.environ.get('AZURE_LOG_INGESTION_ENDPOINT'))
    config.setdefault('rule_id', os.environ.get('AZURE_LOG_INGESTION_RULE_ID'))
    config.setdefault('stream_name', os.environ.get('AZURE_LOG_INGESTION_STREAM_NAME'))
    config.setdefault('table_name', os.environ.get('AZURE_LOG_QUERY_TABLE_NAME', 'AppLogs'))
    config.setdefault('top', 50)
    return config


def utc_now_iso():
    return datetime.now(timezone.utc).isoformat()


def create_credential():
    return DefaultAzureCredential()


def create_query_client():
    return LogsQueryClient(DefaultAzureCredential())


def build_kql(table_name, start_time, end_time, filters=None, severity=None, limit=50):
    clauses = [f"{table_name}"]
    where = []
    if start_time:
        where.append(f"TimeGenerated >= datetime({start_time})")
    if end_time:
        where.append(f"TimeGenerated <= datetime({end_time})")
    if severity:
        where.append(f"tolower(severity) == tolower('{severity}')")
    for key, value in (filters or {}).items():
        where.append(f"tostring({key}) == '{str(value).replace("'", "''")}'")
    if where:
        clauses.append('| where ' + ' and '.join(where))
    clauses.append('| order by TimeGenerated desc')
    clauses.append(f'| take {int(limit)}')
    return ' '.join(clauses)
