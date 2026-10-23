# Define local request, response, and normalization helpers for Managed Metrics Monitoring
from typing import TypedDict, List, Literal

# Request models for metric queries

class MetricQueryRequest(TypedDict):
    resource_id: str
    metric_name: str
    start_time: str  # ISO 8601, e.g. 2025-08-15T12:00:00Z
    end_time: str    # ISO 8601
    # Optional filter string for dimensions, provider-specific syntax
    filter: str | None = None

# Response models

class MetricDataPoint(TypedDict):
    timestamp: str
    value: float | int
    # Optional dimension columns when using multi-dimensional queries
    dimensions: dict[str, str] | None = None

class MetricResponse(TypedDict):
    cost: float | None = None  # Optional provider-specific cost info
    data: List[MetricDataPoint]

# Normalization functions (local helpers) – keep simple for example

def normalize_metric(metric: dict[str, Any]) -> MetricDataPoint:
    """Convert a provider raw metric entry into a common shape."""
    timestamp = metric.get('timestamp')
    value = metric.get('total') or metric.get('average')
    dims = metric.get('dimensions')
    return {
        'timestamp': timestamp,
        'value': value,
        'dimensions': dims
    }
