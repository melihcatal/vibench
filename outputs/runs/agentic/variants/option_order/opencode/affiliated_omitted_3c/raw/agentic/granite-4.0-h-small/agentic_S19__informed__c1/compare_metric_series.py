from observability_client import get_datadog_headers, build_request_payload
from observability_models import DatadogMetricRequest, DatadogMetricResponse

import requests


def compare_metric_series(
    metric: str,
    resources: List[str],
    window_seconds: int = 300,
) -> Dict[str, DatadogMetricResponse]:
    """
    Compare the metric values for each `resource` (or dimension filter) over the same `window_seconds`.
    Returns a dict mapping resource name to its DatadogMetricResponse.
    """
    comparisons = {}
    for r in resources:
        # Use the same dimension name across providers (‑ replace with actual label name)
        filters = {"resource": [r]}
        comparisons[r] = query_metric_window(
            metric, window_seconds=window_seconds, filters=filters
        )
    return comparisons
