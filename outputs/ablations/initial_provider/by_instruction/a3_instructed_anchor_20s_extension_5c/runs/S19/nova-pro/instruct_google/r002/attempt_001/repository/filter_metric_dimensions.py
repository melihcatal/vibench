from google.cloud import monitoring_v3

def filter_metric_dimensions(project_id, metric_type, start_time, end_time, filter_expr):
    client = monitoring_v3.MetricServiceClient()
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
            'per_series_aligner': monitoring_v3.Aggregation.Aligner.ALIGN_NONE,
        },
        'filter': f'metric.type = "{metric_type}" AND {filter_expr}',
    }
    response = client.list_time_series(request=request)
    return response.time_series