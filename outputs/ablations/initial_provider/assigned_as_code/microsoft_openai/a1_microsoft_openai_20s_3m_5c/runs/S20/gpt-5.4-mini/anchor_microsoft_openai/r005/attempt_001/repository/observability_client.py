import os
from azure.identity import DefaultAzureCredential
from azure.monitor.query import LogsQueryClient


def get_observability_config(config=None):
    config = config or {}
    merged = {
        "workspace_id": config.get("workspace_id") or os.environ.get("AZURE_LOG_ANALYTICS_WORKSPACE_ID"),
        "endpoint": config.get("endpoint") or os.environ.get("AZURE_MONITOR_ENDPOINT"),
        "table": config.get("table") or os.environ.get("AZURE_MONITOR_TABLE", "AppTraces"),
        "rule_id": config.get("rule_id") or os.environ.get("AZURE_MONITOR_DCR_RULE_ID"),
        "stream_name": config.get("stream_name") or os.environ.get("AZURE_MONITOR_STREAM_NAME"),
    }
    return merged


def get_logs_query_client():
    return LogsQueryClient(DefaultAzureCredential())


def build_kql(table, where_clauses=None, limit=100, order_desc=True):
    where_clauses = where_clauses or []
    query = table
    if where_clauses:
        query += "\n| where " + " and ".join(where_clauses)
    query += "\n| order by TimeGenerated {}".format("desc" if order_desc else "asc")
    query += "\n| take {}".format(int(limit))
    return query
