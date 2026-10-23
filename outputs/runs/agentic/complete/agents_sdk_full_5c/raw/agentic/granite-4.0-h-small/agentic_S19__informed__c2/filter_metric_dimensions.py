import os
from observability_client import get_cloudwatch_client
from observability_models import MetricFilterRequest, MetricFilterResponse

def filter_metric_dimensions(namespace, metric_name, start_time, end_time, dimensions=None, period=60):
    """Query metric data filtered by resource labels or dimensions using Amazon CloudWatch Metrics.

    Args:
        namespace (str): CloudWatch namespace.
        metric_name (str): Metric identifier.
        start_time (str): ISO8601 start timestamp.
        end_time (str): ISO8601 end timestamp.
        dimensions (list): Optional list of {"Name": ..., "Value": ...} dicts.
        period (int): Granularity in seconds.

    Returns:
        list: Datapoints matching the filter criteria.
    """
    client = get_cloudwatch_client()
    req = {
        "Namespace": namespace,
        "MetricName": metric_name,
        "StartTime": start_time,
        "EndTime": end_time,
        "Period": period,
    }
    if dimensions:
        req["Dimensions"] = dimensions
    response = client.get_metric_statistics(**req)
    return response.get("Datapoints", [])

if __name__ == "__main__":
    # Example: filter CPUUtilization by InstanceId dimension.
    start = os.getenv("AWS_START_TIME") or "2024-08-20T00:00:00Z"
    end = os.getenv("AWS_END_TIME") or "2024-08-20T01:00:00Z"
    dims = [
        {"Name": "InstanceId", "Value": os.getenv("AWS_INSTANCE_ID")}
    ]
    pts = filter_metric_dimensions(
        os.getenv("AWS_NAMESPACE"),
        os.getenv("AWS_METRIC_NAME"),
        start,
        end,
        dimensions=dims,
    )
    print(f"Filtered datapoints count: {len(pts)}")
