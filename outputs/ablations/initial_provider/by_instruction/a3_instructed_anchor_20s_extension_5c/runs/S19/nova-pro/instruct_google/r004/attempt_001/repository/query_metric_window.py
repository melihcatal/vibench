from google.cloud import monitoring_v3

def query_metric_window(project_id, metric_type, start_time, end_time):
    client = monitoring_v3.MetricServiceClient()
    name = f'projects/{project_id}'
    interval = {
        'start_time': start_time,
        'end_time': end_time,
    }
    request = {
        'name': name,
        'interval': interval,
        'filter': f'metric.type = "{metric_type}"',
    }
    response = client.list_time_series(request=request)
    return response