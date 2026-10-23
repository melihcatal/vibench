from observability_client import get_query_client, load_observability_config
from observability_models import extract_table_rows


def fetch_recent_logs(payload, config=None):
    settings = load_observability_config(config)
    query_client = get_query_client()
    start_time = payload['start_time']
    end_time = payload['end_time']
    field_name = payload['field_name']
    field_value = payload['field_value']
    query = f"AppTraces | where {field_name} == '{field_value}' | order by TimeGenerated desc"
    response = query_client.query_workspace(settings.workspace_id, query, timespan=(start_time, end_time))
    return {'records': extract_table_rows(response)}
