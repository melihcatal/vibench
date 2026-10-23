from azure.monitor.query import LogsQueryStatus

from observability_client import build_kql, get_logs_query_client, get_observability_config


def fetch_recent_logs(payload, config=None):
    config = get_observability_config(config)
    clauses = []
    for key, value in (payload.get("field_values") or {}).items():
        clauses.append("{} == '{}'".format(key, value))
    if payload.get("start_time"):
        clauses.append("TimeGenerated >= datetime({})".format(payload["start_time"]))
    if payload.get("end_time"):
        clauses.append("TimeGenerated <= datetime({})".format(payload["end_time"]))
    query = build_kql(config["table"], clauses, limit=payload.get("limit", 50))
    client = get_logs_query_client()
    result = client.query_workspace(config["workspace_id"], query, timespan=None)
    rows = []
    if result.status == LogsQueryStatus.SUCCESS:
        for row in result.tables[0].rows:
            rows.append(dict(zip(result.tables[0].columns, row)))
    return {"query": query, "rows": rows}
