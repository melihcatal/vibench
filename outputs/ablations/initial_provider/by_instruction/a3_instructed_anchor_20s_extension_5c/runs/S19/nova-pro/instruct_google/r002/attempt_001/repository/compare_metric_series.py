from google.cloud import monitoring_v3

def compare_metric_series(project_id, metric_type, start_time, end_time, filter_expr1, filter_expr2):
    client = monitoring_v3.MetricServiceClient()
    name = f'projects/{project_id}'
    interval = {
        'start_time': start_time,
        'end_time': end_time,
    }
    request1 = {
        'name': name,
        'interval': interval,
        'aggregation': {
            'alignment_period': {'seconds': 60},
            'per_series_aligner': monitoring_v3.Aggregation.Aligner.ALIGN_NONE,
        },
        'filter': f'metric.type = "{metric_type}" AND {filter_expr1}',
    }
    request2 = {
        'name': name,
        'interval': interval,
        'aggregation': {
            'alignment_period': {'seconds': 60},
            'per_series_aligner': monitoring_v3.Aggregation.Aligner.ALIGN_NONE,
        },
        'filter': f'metric.type = "{metric_type}" AND {filter_expr2}',
    }
    response1 = client.list_time_series(request=request1)
    response2 = client.list_time_series(request=request2)
    return response1.time_series, response2.time_series