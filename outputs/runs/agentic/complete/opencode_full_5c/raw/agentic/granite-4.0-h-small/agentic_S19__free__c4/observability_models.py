# [HELPER] observability_models.py
from typing import TypedDict, List, Dict, Any


class MetricQueryRequest(TypedDict):
    metric: str
    start: str  # ISO timestamp
    end: str  # ISO timestamp
    filter: str = None
    resource_a: str = None
    resource_b: str = None


class MetricResponse(TypedDict):
    series: List[Dict[str, Any]]
    meta: Dict[str, Any]


class MetricStatsResponse(TypedDict):
    sum: float
    avg: float
    min: float
    max: float


class FilteredMetricResponse(MetricResponse):
    # Additional fields specific to filtered queries can be added here
    pass


# Normalization helpers -- convert provider-specific response to a uniform format


def normalize_response(raw: Dict[str, Any]) -> MetricResponse:
    """Convert provider-specific payload to the standard MetricResponse shape."""
    # Example transformation for Datadog API response
    # data = raw['series']
    # return MetricResponse(series=data, meta={})
    return MetricResponse(series=[], meta={})


def normalize_stats(raw: Dict[str, Any]) -> MetricStatsResponse:
    """Extract and normalize stats from provider response."""
    return MetricStatsResponse(
        sum=raw.get("sum", 0),
        avg=raw.get("avg", 0),
        min=raw.get("min", 0),
        max=raw.get("max", 0),
    )


# Additional helpers for filtering, comparing, etc., can be added here
