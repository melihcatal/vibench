import google.auth
from google.cloud import monitoring_v3

def compare_metric_series(project_id, metric_type, start_time, end_time, filter1, filter2):
    credentials, project = google.auth.default()
    client = monitoring_v3.MetricServiceClient(credentials=credentials)
    name = f'projects/{project_id}'
    interval = {
        'start_time': start_time,
        'end_time': end_time,
    }
    request1 = {
        'name': name,
        'interval': interval,
        'filter': f'metric.type = "{metric_type}" AND {filter1}',
    }
    request2 = {
        'name': name,
        'interval': interval,
        'filter': f'metric.type = "{metric_type}" AND {filter2}',
    }
    response1 = client.list_time_series(request=request1)
    response2 = client.list_time_series(request=request2)
    return response1.time_series, response2.time_series