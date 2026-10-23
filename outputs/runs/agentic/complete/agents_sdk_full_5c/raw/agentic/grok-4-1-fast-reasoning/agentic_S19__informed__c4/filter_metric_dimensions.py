from typing import List, Tuple, Dict
from datetime import datetime
from observability_client import get_cloudwatch_client
from observability_models import build_metric_data_query, recent_time_window, MetricStat

def filter_metric_dimensions(
    metric_name: str,
    dimensions: List[Dict[str, str]],
    minutes: int = 60,
    namespace: str = 'AWS/EC2'
) -> List[Tuple[datetime, float]]:
    """Query metric data filtered by resource labels or dimensions."""
    client = get_cloudwatch_client()
    start, end = recent_time_window(minutes)
    stat = MetricStat(metric_name=metric_name, namespace=namespace, dimensions=dimensions)
    mdq = build_metric_data_query('m1', stat)
    response = client.get_metric_data(
        MetricDataQueries=[mdq],
        StartTime=start,
        EndTime=end
    )
    result = response['MetricDataResults'][0]
    values = list(zip(result['Timestamps'], result['Values']))
    return values