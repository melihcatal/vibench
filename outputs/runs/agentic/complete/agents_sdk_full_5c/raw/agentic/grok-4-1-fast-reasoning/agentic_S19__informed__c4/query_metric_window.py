from typing import List, Tuple
from datetime import datetime, float
from observability_client import get_cloudwatch_client
from observability_models import build_metric_data_query, recent_time_window, MetricStat

def query_metric_window(metric_name: str, minutes: int = 60, namespace: str = 'AWS/EC2') -> List[Tuple[datetime, float]]:
    """Query recent datapoints for named metric over time window."""
    client = get_cloudwatch_client()
    start, end = recent_time_window(minutes)
    stat = MetricStat(metric_name=metric_name, namespace=namespace)
    mdq = build_metric_data_query('m1', stat)
    response = client.get_metric_data(
        MetricDataQueries=[mdq],
        StartTime=start,
        EndTime=end
    )
    result = response['MetricDataResults'][0]
    values = list(zip(result['Timestamps'], result['Values']))
    return values