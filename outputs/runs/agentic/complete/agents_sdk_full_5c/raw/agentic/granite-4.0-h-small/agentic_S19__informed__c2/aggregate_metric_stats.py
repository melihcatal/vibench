import os
from observability_client import get_cloudwatch_client
from observability_models import MetricStatisticsRequest, MetricStatisticsResponse

def aggregate_metric_stats(namespace, metric_name, start_time, end_time, statistics=None):
    """Retrieve aggregated statistics for a metric over a time window using Amazon CloudWatch Metrics.

    Args:
        namespace (str): CloudWatch namespace.
        metric_name (str): Name of the metric.
        start_time (str): ISO8601 start timestamp.
        end_time (str): ISO8601 end timestamp.
        statistics (list): Optional list of statistic strings (e.g., ['Minimum', 'Maximum', 'Sum']).

    Returns:
        dict: Aggregated statistics response from CloudWatch.
    """
    client = get_cloudwatch_client()
    req = {
        "Namespace": namespace,
        "MetricName": metric_name,
        "StartTime": start_time,
        "EndTime": end_time,
        "Period": 300,  # 5-minute granularity
    }
    if statistics:
        req["Statistics"] = statistics
    response = client.get_metric_statistics(**req)
    return response

if __name__ == "__main__":
    # Demo: pull Max, Avg, and SampleCount for CPUUtilization over the last hour.
    import datetime
    now = datetime.datetime.utcnow().isoformat() + "Z"
    hour_ago = (datetime.datetime.utcnow() - datetime.timedelta(hours=1)).isoformat() + "Z"
    stats = aggregate_metric_stats(
        os.getenv("AWS_NAMESPACE"),
        os.getenv("AWS_METRIC_NAME"),
        hour_ago,
        now,
        statistics=["Maximum", "Average", "SampleCount"],
    )
    print(stats)
