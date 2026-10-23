from datetime import datetime, timezone

from azure.monitor.query import LogsQueryStatus

from observability_client import get_query_client, load_observability_config
from observability_models import extract_table_rows


def query_error_logs(payload, config=None):
    settings = load_observability_config(config)
    query_client = get_query_client()
    start_time = payload['start_time'].astimezone(timezone.utc)
    end_time = payload['end_time'].astimezone(timezone.utc)
    severity = payload.get('severity', 'Error')
    query = f"AppTraces | where SeverityLevel == '{severity}' | where TimeGenerated between (datetime({start_time.isoformat()}) .. datetime({end_time.isoformat()})) | order by TimeGenerated desc"
    response = query_client.query_workspace(settings.workspace_id, query, timespan=(start_time, end_time))
    rows = extract_table_rows(response)
    if getattr(response, 'status', None) == LogsQueryStatus.PARTIAL:
        return {'status': 'partial', 'records': rows}
    return {'status': 'success', 'records': rows}
