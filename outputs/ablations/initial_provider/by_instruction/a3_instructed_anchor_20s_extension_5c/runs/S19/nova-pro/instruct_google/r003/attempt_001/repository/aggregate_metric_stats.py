import google.auth
from google.cloud import monitoring_v3

def aggregate_metric_stats(project_id, metric_type, start_time, end_time):
    credentials, project = google.auth.default()
    client = monitoring_v3.MetricServiceClient(credentials=credentials)
    name = f'projects/{project_id}'
    interval = {
        'start_time': start_time,
        'end_time': end_time,
    }
    request = {
        'name': name,
        'interval': interval,
        'filter': f'metric.type = "{metric_type}"',
        'aggregation': {
            'alignment_period': {'seconds': 60},
            'per_series_aligner': 'ALIGN_MEAN',
            'cross_series_reducer': 'REDUCE_NONE',
            'group_by_fields': ['resource.type'],
        },
    }
    response = client.list_time_series(request=request)
    return response.time_series