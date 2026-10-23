from observability_client import get_client, get_project_id
from observability_models import TimeSeriesRequest

def metric_summary(metric_type, start_time, end_time):
    client = get_client()
    project_id = get_project_id()
    request = TimeSeriesRequest(project_id, metric_type, start_time, end_time)
    response = client.list_time_series(request=request.to_proto())
    return response.time_series