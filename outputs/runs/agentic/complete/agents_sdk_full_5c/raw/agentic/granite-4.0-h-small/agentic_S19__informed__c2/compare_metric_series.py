import os
from observability_client import get_cloudwatch_client
from observability_models import MetricSeriesRequest, MetricSeriesResponse

def compare_metric_series(namespace_a, metric_name, start_a, end_a, namespace_b=None, dimensions_a=None, dimensions_b=None, period=300):
    """Compare metric values for two resources or dimension filters over the same window using Amazon CloudWatch Metrics.

    Args:
        namespace_a (str): CloudWatch namespace for series A.
        metric_name (str): Metric identifier (same for A and B).
        start_a (str): ISO8601 start for series A.
        end_a (str): ISO8601 end for series A (also used for B).
        namespace_b (str): Optional alternate namespace for series B.
        dimensions_a (list): Optional dimension filters for series A.
        dimensions_b (list): Optional dimension filters for series B.
        period (int): Granularity in seconds.

    Returns:
        tuple: (datapoints_a, datapoints_b) as lists of dicts.
    """
    client = get_cloudwatch_client()
    def get_series(ns, dims):
        req = {
            "Namespace": ns,
            "MetricName": metric_name,
            "StartTime": start_a,
            "EndTime": end_a,
            "Period": period,
        }
        if dims:
            req["Dimensions"] = dims
        resp = client.get_metric_statistics(**req)
        return resp.get("Datapoints", [])

    dp_a = get_series(namespace_a, dimensions_a)
    dp_b = get_series(namespace_b or namespace_a, dimensions_b)
    return dp_a, dp_b

if __name__ == "__main__":
    # Compare CPUUtilization between two EC2 instances over the last 2 hours.
    start = os.getenv("AWS_START_TIME", "2024-08-20T10:00:00Z")
    end = os.getenv("AWS_END_TIME", "2024-08-20T12:00:00Z")
    dims_a = [{"Name": "InstanceId", "Value": os.getenv("INSTANCE_A_ID")}]
    dims_b = [{"Name": "InstanceId", "Value": os.getenv("INSTANCE_B_ID")}]
    series_a, series_b = compare_metric_series(
        os.getenv("AWS_NAMESPACE"),
        os.getenv("AWS_METRIC_NAME"),
        start,
        end,
        dimensions_a=dims_a,
        dimensions_b=dims_b,
    )
    print(f"Series A count: {len(series_a)}")
    print(f"Series B count: {len(series_b)}")
