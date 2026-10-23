from google.cloud import monitoring_v3

def aggregate_metric_stats(project_id, metric_type, start_time, end_time):
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
            'per_series_aligner': monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
        },
        'filter': f'metric.type = "{metric_type}"',
    }
    response = client.list_time_series(request)
    return response
