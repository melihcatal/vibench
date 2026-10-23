from observability_client import client
from observability_models import MetricQuery, MetricResponse

def query_metric_window(metric_name: str, start_time: str, end_time: str):
    query = MetricQuery(metric_name, {'aggregation': 'Average'}, f'{start_time}/{end_time}')
    response = client.query_metrics(query)
    return MetricResponse(response.name, response.timeseries)