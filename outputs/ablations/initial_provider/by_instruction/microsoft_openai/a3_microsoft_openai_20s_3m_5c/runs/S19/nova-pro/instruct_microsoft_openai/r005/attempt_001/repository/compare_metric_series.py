from observability_client import client
from observability_models import MetricQuery, MetricResponse

def compare_metric_series(metric_name: str, dimension_filter1: Dict[str, str], dimension_filter2: Dict[str, str], start_time: str, end_time: str):
    query1 = MetricQuery(metric_name, {'aggregation': 'Average', 'dimensions': dimension_filter1}, f'{start_time}/{end_time}')
    query2 = MetricQuery(metric_name, {'aggregation': 'Average', 'dimensions': dimension_filter2}, f'{start_time}/{end_time}')
    response1 = client.query_metrics(query1)
    response2 = client.query_metrics(query2)
    return MetricResponse(response1.name, response1.timeseries), MetricResponse(response2.name, response2.timeseries)