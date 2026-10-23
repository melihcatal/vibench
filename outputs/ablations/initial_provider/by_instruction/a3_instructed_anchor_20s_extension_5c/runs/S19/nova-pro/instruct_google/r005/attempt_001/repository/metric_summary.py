from google.cloud import monitoring_v3
from observability_client import get_client, get_project_id

def metric_summary(metric_type, start_time, end_time):
    client = get_client()
    project_id = get_project_id()
    name = f'projects/{project_id}'
    interval = {
        'start_time': start_time,
        'end_time': end_time,
    }
    request = {
        'name': name,
        'interval': interval,
        'aggregation': {
            'alignment_period': {'seconds': 60},
            'per_series_aligner': monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
        },
        'filter': f'metric.type = "{metric_type}"',
    }
    response = client.list_time_series(request)
    return response
