# [SAME-SCENARIO] compare_metric_series.py

from observability_client import CloudWatchClient
from observability_models import CompareMetricRequest, CompareMetricResponse

def compare_metric_series(namespace: str, metric_name: str, dimension_filter_a: dict, dimension_filter_b: dict, start_time: str, end_time: str) -> CompareMetricResponse:
    """Compare metric values for two resources or dimension filters over the same window using Amazon CloudWatch.

    Args:
        namespace (str): CloudWatch namespace.
        metric_name (str): Metric name.
        dimension_filter_a (dict): First set of dimension filters.
        dimension_filter_b (dict): Second set of dimension filters.
        start_time (str): ISO8601 start time.
        end_time (str): ISO8601 end time.

    Returns:
        CompareMetricResponse: Normalized response containing side‑by‑side datapoints.
    """
    client = CloudWatchClient()
    request = CompareMetricRequest(
        Namespace=namespace,
        MetricName=metric_name,
        StartTime=start_time,
        EndTime=end_time,
        DimensionFilters=[dimension_filter_a, dimension_filter_b]
    )
    response = client.get_metric_data(request)
    return response