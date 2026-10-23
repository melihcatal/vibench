from azure.identity import DefaultAzureCredential
from azure.monitor.query import LogsQueryClient

from observability_models import coerce_rows


def query_error_logs(payload, config=None):
    config = config or {}
    query = config.get("query") or payload["query"]
    timespan = config.get("timespan") or payload.get("timespan")
    with DefaultAzureCredential() as credential:
        client = LogsQueryClient(credential=credential)
        result = client.query_workspace(workspace_id=config["workspace_id"], query=query, timespan=timespan)
    table = result.tables[0] if result.tables else None
    rows = coerce_rows(table.rows) if table else []
    return {"rows": rows, "status": result.status.name if hasattr(result.status, "name") else str(result.status)}
