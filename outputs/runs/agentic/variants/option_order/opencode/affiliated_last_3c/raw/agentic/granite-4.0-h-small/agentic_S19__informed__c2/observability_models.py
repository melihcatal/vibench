# [HELPER] observability_models.py

# Local request/response models for Managed Metrics Monitoring.
# Provider: Amazon CloudWatch Metrics (boto3 SDK)

from typing import List, Dict, Any


class CloudWatchMetricQuery:
    """Request model for querying raw metric datapoints."""

    def __init__(
        self,
        namespace: str,
        metric_name: str,
        start_time: str,
        end_time: str,
        period: int,
        statistics: List[str] = None,
        dimensions: List[Dict[str, Any]] = None,
    ):
        self.namespace = namespace
        self.metric_name = metric_name
        self.start_time = start_time  # ISO 8601 string
        self.end_time = end_time  # ISO 8601 string
        self.period = period
        self.statistics = statistics or ["Average"]
        self.dimensions = dimensions or []


class CloudWatchMetricStatQuery:
    """Request model for aggregated metric statistics."""

    def __init__(
        self,
        namespace: str,
        metric_name: str,
        start_time: str,
        end_time: str,
        period: int,
        statistics: List[str],
        dimensions: List[Dict[str, Any]] = None,
    ):
        self.namespace = namespace
        self.metric_name = metric_name
        self.start_time = start_time
        self.end_time = end_time
        self.period = period
        self.statistics = statistics
        self.dimensions = dimensions or []


class MetricDatapointsResponse:
    """Normalized response wrapper for metric datapoints."""

    def __init__(self, data: List[Dict[str, Any]]):
        self.timestamp = data.get("Timestamp")
        self.value = data.get("Value")
        self.unit = data.get("Unit")


class MetricAggregateResponse:
    """Normalized response wrapper for aggregated statistics."""

    def __init__(self, data: List[Dict[str, Any]]):
        self.label = data.get("Label")
        self.value = data.get("Value")
        self.unit = data.get("Unit")


# Example normalization helper-------------------------------------------


def normalize_metric_response(
    raw: Dict[str, Any],
) -> List[MetricDatapointsResponse] | List[MetricAggregateResponse]:
    """Convert raw CloudWatch JSON into domain-specific model.

    Returns list of MetricDatapointsResponse for raw queries,
    or MetricAggregateResponse for aggregated stats.
    """

    # Distinguish by presence of 'Datapoints' vs 'MetricDataResults'
    if "Datapoints" in raw:
        return [MetricDatapointsResponse(dp) for dp in raw["Datapoints"]]
    elif "MetricDataResults" in raw:
        return [MetricAggregateResponse(r) for r in raw["MetricDataResults"]]
    else:
        raise ValueError("Unexpected response structure")
