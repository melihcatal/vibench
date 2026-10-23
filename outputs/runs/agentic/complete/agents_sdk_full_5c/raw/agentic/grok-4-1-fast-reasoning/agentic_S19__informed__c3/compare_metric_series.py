from observability_client import cloudwatch_client, get_time_window
from observability_models import extract_averages
from typing import List, Dict, Any

def compare_metric_series(metric_name: str, dimensions1: List[Dict[str, str]], dimensions2: List[Dict[str, str]], namespace: str = 'AWS/EC2', hours: float = 1.0) -> Dict[str, float]:
    start_time, end_time = get_time_window(hours)
    resp1 = cloudwatch_client.get_metric_statistics(
        Namespace=namespace, MetricName=metric_name, Dimensions=dimensions1,
        StartTime=start_time, EndTime=end_time, Period=300, Statistics=['Average']
    )
    resp2 = cloudwatch_client.get_metric_statistics(
        Namespace=namespace, MetricName=metric_name, Dimensions=dimensions2,
        StartTime=start_time, EndTime=end_time, Period=300, Statistics=['Average']
    )
    avgs1 = extract_averages(resp1.get('Datapoints', []))
    avgs2 = extract_averages(resp2.get('Datapoints', []))
    if not avgs1 or not avgs2:
        return {'series1_last_avg': 0.0, 'series2_last_avg': 0.0, 'absolute_difference': 0.0, 'percent_difference': 0.0}
    last1 = avgs1[-1]
    last2 = avgs2[-1]
    diff = last1 - last2
    pct_diff = (diff / last2 * 100) if last2 != 0 else 0.0
    return {
        'series1_last_avg': last1,
        'series2_last_avg': last2,
        'absolute_difference': diff,
        'percent_difference': pct_diff
    }