# [LATER-STEP] metric_summary.py
import os
from datetime import datetime, timedelta
from observability_client import Boto3Client
from observability_models import MetricRequest, MetricResponse

def summarize_recent_trends(metric_name: str, namespace: str = None, dimensions: dict = None, window_hours: int = 2):
    """Summarize recent metric trends or anomalies for a metric using CloudWatch Insights.
    This simple example queries the metric over the window and reports basic statistics.
    Args:
        metric_name: Name of the metric.
        namespace: CloudWatch namespace (e.g., "AWS/EC2").
        dimensions: Optional dimension filters.
        window_hours: Lookback hours.
    Returns:
        A dict summarizing count, average, min, max, and a basic anomaly flag.
    """
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=window_hours)
    request = MetricRequest(
        metric_name=metric_name,
        namespace=namespace,
        dimensions=dimensions,
        start_time=start_time.isoformat() + 'Z',
        end_time=end_time.isoformat() + 'Z',
        period=300,  # 5 minutes
    )
    client = Boto3Client(service="cloudwatch")
    response = client.get_metric_statistics(request)
    datapoints = response.datapoints
    values = [dp.Value for dp in datapoints]
    summary = {
        "count": len(values),
        "average": sum(values) / len(values) if values else None,
        "min": min(values) if values else None,
        "max": max(values) if values else None,
        "anomaly_flag": len(values) > 5 and max(values) > (2 * sum(v for v in values if v < max(values)) / (len(values) - 1)),
    }
    return summary

if __name__ == "__main__":
    print(summarize_recent_trends("CPUUtilization"))
