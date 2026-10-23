from observability_client import client
from observability_models import MetricQuery, MetricResponse

def filter_metric_dimensions(metric_name: str, dimensions: Dict[str, str], start_time: str, end_time: str):
    query = MetricQuery(metric_name, {'aggregation': 'Average', 'dimensions': dimensions}, f'{start_time}/{end_time}')
    response = client.query_metrics(query)
    return MetricResponse(response.name, response.timeseries)