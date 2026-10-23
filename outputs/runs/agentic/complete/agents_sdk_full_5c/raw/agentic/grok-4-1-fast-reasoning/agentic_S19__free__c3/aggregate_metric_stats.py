import boto3
from typing import List
from statistics import stdev
from datetime import timezone
from observability_client import get_recent_time_window
from observability_models import MetricDatapoint, MetricStats

def aggregate_metric_stats(
    namespace: str,
    metric_name: str,
    duration_minutes: int = 60,
    period: int = 300
) -> MetricStats:
    client = boto3.client('cloudwatch')
    start_time, end_time = get_recent_time_window(duration_minutes)
    response = client.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=['Average', 'Minimum', 'Maximum', 'Sum', 'SampleCount'],
    )
    datapoints = response.get('Datapoints', [])
    if not datapoints:
        return MetricStats(average=0.0, min_=0.0, max_=0.0, sum_=0.0, count=0)

    avgs = [dp.get('Average') for dp in datapoints if dp.get('Average') is not None]
    mins = [dp.get('Minimum') for dp in datapoints if dp.get('Minimum') is not None]
    maxs = [dp.get('Maximum') for dp in datapoints if dp.get('Maximum') is not None]
    sums = [dp.get('Sum') or 0.0 for dp in datapoints]
    counts = [dp.get('SampleCount') or 0 for dp in datapoints]

    overall_avg = sum(avgs) / len(avgs) if avgs else 0.0
    overall_min = min(mins) if mins else 0.0
    overall_max = max(maxs) if maxs else 0.0
    total_sum = sum(sums)
    total_count = sum(counts)
    stddev_val = stdev(avgs) if len(avgs) > 1 else None

    return MetricStats(
        average=overall_avg,
        min_=overall_min,
        max_=overall_max,
        sum_=total_sum,
        count=total_count,
        stddev=stddev_val
    )