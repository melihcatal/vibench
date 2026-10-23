# filter_metric_dimensions.py

from __future__ import annotations

import json
from typing import Any, Dict, List

from observability_client import get_metrics_client
from observability_models import RequestModel, NormalizedMetricResponse, DimensionFilter

# ---------------------------------------------------------------------------
# Configuration (choose ONE concrete provider)
# ---------------------------------------------------------------------------
# Example: IBM Cloud Monitoring
IBM_MONITORING_INSTANCE_ID = "YOUR_MONITORING_INSTANCE_ID"
IBM_CLOUD_API_KEY = "YOUR_IBM_CLOUD_API_KEY"

# Example: Amazon CloudWatch Metrics (uncomment if using AWS)
# AWS_ACCESS_KEY_ID = "YOUR_AWS_ACCESS_KEY_ID"
# AWS_SECRET_ACCESS_KEY = "YOUR_AWS_SECRET_ACCESS_KEY"

# Example: Datadog (uncomment if using Datadog)
# DD_API_KEY = "YOUR_DATADOG_API_KEY"
# DD_APP_KEY = "YOUR_DATADOG_APP_KEY"

# ---------------------------------------------------------------------------
# Helper: build a concrete query payload for the selected service
# ---------------------------------------------------------------------------


def build_query_payload(
    metric_name: str, start_time: int, end_time: int, filters: List[DimensionFilter]
) -> RequestModel:
    """Create a request payload that includes dimension filters."
    The dict matches the abstraction used by get_metrics_client.
    """
    payload: RequestModel = {
        "metric": metric_name,
        "start": start_time,
        "end": end_time,
        "filters": filters,
    }
    return payload


# ---------------------------------------------------------------------------
# Core integration function
# ---------------------------------------------------------------------------


def filter_metric_dimensions(
    metric_name: str, start: int, end: int, filters: List[DimensionFilter]
) -> NormalizedMetricResponse:
    """Query metric data filtered by the supplied dimension criteria."

    Args:
        metric_name: Name of the metric to filter.
        start: Unix epoch start time (seconds).
        end: Unix epoch end time (seconds).
        filters: List of dimension filters, e.g. [{"resource_id": "i-123"}, {"region": "us-east-1"}].

    Returns: Normalized response containing only matching datapoints.
    """
    client = get_metrics_client()
    raw_response: Dict[str, Any] = client.filtered(
        payload=build_query_payload(metric_name, start, end, filters)
    )
    return normalize_response(raw_response)


# ---------------------------------------------------------------------------
# Example usage (for local testing only)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import time

    now = int(time.time())
    five_min_ago = now - 300
    filters = [{"resource_id": "i-0abcd1234"}, {"region": "us-east-1"}]
    result = filter_metric_dimensions(
        "disk.iops", start=five_min_ago, end=now, filters=filters
    )
    print(json.dumps(result, indent=2))
