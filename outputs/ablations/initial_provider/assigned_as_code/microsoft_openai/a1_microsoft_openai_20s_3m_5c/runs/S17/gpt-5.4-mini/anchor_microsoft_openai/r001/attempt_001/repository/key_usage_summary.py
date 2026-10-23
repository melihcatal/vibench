from azure.identity import DefaultAzureCredential
from azure.monitor.query import LogsQueryClient


def key_usage_summary(payload=None, config=None):
    config = config or {}
    payload = payload or {}
    query = payload.get("query", "AzureDiagnostics | summarize count() by OperationName")
    with DefaultAzureCredential() as credential:
        client = LogsQueryClient(credential)
        result = client.query_workspace(config["workspace_id"], query, timespan=payload.get("timespan"))
    return {"query": query, "tables": [table.name for table in getattr(result, "tables", [])]}
