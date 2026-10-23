from azure.monitor.query import LogsQueryStatus

from observability_client import build_kql, get_logs_query_client, get_observability_config


def query_error_logs(payload, config=None):
    config = get_observability_config(config)
    clauses = ["SeverityLevel >= 3"]
    if payload.get("service_name"):
        clauses.append("ServiceName == '{}'".format(payload["service_name"]))
    if payload.get("request_id"):
        clauses.append("request_id == '{}'".format(payload["request_id"]))
    if payload.get("start_time"):
        clauses.append("TimeGenerated >= datetime({})".format(payload["start_time"]))
    if payload.get("end_time"):
        clauses.append("TimeGenerated <= datetime({})".format(payload["end_time"]))
    query = build_kql(config["table"], clauses, limit=payload.get("limit", 100))
    client = get_logs_query_client()
    result = client.query_workspace(config["workspace_id"], query, timespan=None)
    rows = []
    if result.status == LogsQueryStatus.SUCCESS:
        for row in result.tables[0].rows:
            rows.append(dict(zip(result.tables[0].columns, row)))
    return {"query": query, "rows": rows}
