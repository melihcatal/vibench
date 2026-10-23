import google.auth
from google.cloud import monitoring_v3

def filter_metric_dimensions(project_id, metric_type, start_time, end_time, filter_):
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
        'filter': f'metric.type = "{metric_type}" AND {filter_}',
    }
    response = client.list_time_series(request=request)
    return response.time_series