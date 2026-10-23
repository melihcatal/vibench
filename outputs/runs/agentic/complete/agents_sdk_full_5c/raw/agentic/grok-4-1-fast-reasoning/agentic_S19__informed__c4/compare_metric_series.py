from typing import List, Tuple, Dict
from datetime import datetime
from observability_client import get_cloudwatch_client
from observability_models import build_metric_data_query, recent_time_window, MetricStat

def compare_metric_series(
    metric_name: str,
    dimensions1: List[Dict[str, str]],
    dimensions2: List[Dict[str, str]],
    minutes: int = 60,
    namespace: str = 'AWS/EC2'
) -> Tuple[List[Tuple[datetime, float]], List[Tuple[datetime, float]]]:
    """Compare metric values for two resources or dimension filters."""
    client = get_cloudwatch_client()
    start, end = recent_time_window(minutes)
    stat1 = MetricStat(metric_name=metric_name, namespace=namespace, dimensions=dimensions1)
    stat2 = MetricStat(metric_name=metric_name, namespace=namespace, dimensions=dimensions2)
    mdq1 = build_metric_data_query('series1', stat1)
    mdq2 = build_metric_data_query('series2', stat2)
    response = client.get_metric_data(
        MetricDataQueries=[mdq1, mdq2],
        StartTime=start,
        EndTime=end
    )
    result1 = response['MetricDataResults'][0]
    result2 = response['MetricDataResults'][1]
    series1 = list(zip(result1['Timestamps'], result1['Values']))
    series2 = list(zip(result2['Timestamps'], result2['Values']))
    return series1, series2