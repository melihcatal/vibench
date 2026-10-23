from observability_client import load_config, logs_query_client
from observability_models import make_time_range, normalize_rows


def query_error_logs(payload, config=None):
    cfg = load_config(config)
    start, end = payload.get('start_time'), payload.get('end_time')
    if not start or not end:
        start, end = make_time_range(payload.get('hours', 24))
    severity = payload.get('severity', 'Error')
    query = f"AppLogs | where Severity == '{severity}' | where TimeGenerated between (datetime({start}) .. datetime({end})) | order by TimeGenerated desc"
    client = logs_query_client()
    result = client.query_workspace(cfg['workspace_id'], query, timespan=None)
    rows = []
    if getattr(result, 'tables', None):
        for row in result.tables[0].rows:
            rows.append(dict(zip(result.tables[0].columns, row)))
    return {'rows': normalize_rows(rows), 'severity': severity, 'start_time': start, 'end_time': end}
