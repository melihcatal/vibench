import boto3
from typing import List, Dict
from observability_client import get_recent_time_window
from observability_models import MetricDatapoint

def compare_metric_series(
    namespace1: str,
    metric_name1: str,
    dimensions1: List[Dict[str, str]],
    namespace2: str,
    metric_name2: str,
    dimensions2: List[Dict[str, str]],
    duration_minutes: int = 60,
    period: int = 300
) -> Dict[str, float]:
    client = boto3.client('cloudwatch')
    start_time, end_time = get_recent_time_window(duration_minutes)

    def get_average(ns: str, mn: str, dims: List[Dict[str, str]]) -> float:
        resp = client.get_metric_statistics(
            Namespace=ns,
            MetricName=mn,
            Dimensions=dims,
            StartTime=start_time,
            EndTime=end_time,
            Period=period,
            Statistics=['Average'],
        )
        avgs = [dp.get('Average') for dp in resp.get('Datapoints', []) if dp.get('Average') is not None]
        return sum(avgs) / len(avgs) if avgs else 0.0

    avg1 = get_average(namespace1, metric_name1, dimensions1)
    avg2 = get_average(namespace2, metric_name2, dimensions2)
    ratio = avg1 / avg2 if avg2 != 0 else float('inf')
    diff = avg1 - avg2

    return {
        'series1_average': avg1,
        'series2_average': avg2,
        'ratio': ratio,
        'difference': diff
    }