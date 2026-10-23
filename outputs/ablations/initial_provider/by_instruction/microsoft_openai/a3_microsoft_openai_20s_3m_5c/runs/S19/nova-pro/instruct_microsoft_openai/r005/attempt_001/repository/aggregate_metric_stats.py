from observability_client import client
from observability_models import MetricQuery, MetricResponse

def aggregate_metric_stats(metric_name: str, start_time: str, end_time: str):
    query = MetricQuery(metric_name, {'aggregation': 'Count,Average,Minimum,Maximum'}, f'{start_time}/{end_time}')
    response = client.query_metrics(query)
    return MetricResponse(response.name, response.timeseries)