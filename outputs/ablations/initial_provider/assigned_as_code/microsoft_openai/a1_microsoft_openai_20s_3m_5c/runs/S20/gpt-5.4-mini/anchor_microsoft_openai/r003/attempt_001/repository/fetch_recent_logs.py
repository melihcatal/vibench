from observability_client import build_kql, create_query_client, load_observability_config
from observability_models import LogResponse


def fetch_recent_logs(payload, config=None):
    config = load_observability_config(config)
    query = build_kql(
        config['table_name'],
        payload['start_time'],
        payload['end_time'],
        filters=payload.get('filters'),
        limit=payload.get('limit', config['top']),
    )
    client = create_query_client()
    result = client.query_workspace(config['workspace_id'], query)
    rows = []
    if getattr(result, 'tables', None):
        for row in result.tables[0].rows:
            rows.append(dict(zip(result.tables[0].columns, row)))
    return LogResponse(items=rows, count=len(rows)).__dict__
