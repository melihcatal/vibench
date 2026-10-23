import google.auth
from google.cloud import monitoring_v3
from.observability_client import get_client, get_project_id
from.observability_models import MetricRequest, MetricResponse

def metric_summary(project_id, metric_type, start_time, end_time):
    client = get_client()
    request = MetricRequest(project_id, metric_type, start_time, end_time)
    response = client.list_time_series(request.__dict__)
    return MetricResponse(response.time_series)