# HELPER

from dataclasses import dataclass
from datetime import datetime

# Simple request/response models used by SAME-SCENARIO integration files.

@dataclass

class MetricQueryRequest:
    """Parameters for querying raw datapoints."""
    metric: str
    start: datetime | None = None
    end: datetime | None = None
    tags: list[str] | None = None

@dataclass
class MetricQueryResponse:
    """Structure of Datadog's query response."""
    metric: str
    tags: list[str]
    values: list[list[int, float]]  # [timestamp, value]

@dataclass
class MetricStatsRequest:
    """Parameters for aggregated statistics."""
    metric: str
    start: datetime
    end: datetime
    interval: int = 60
    aggregate: str = 'avg'  # avg, sum, min, max, count, etc.

@dataclass
class MetricStatsResponse:
    metric: str
    aggregated: str
    points: list[list[int, float]]  # may contain nested buckets depending on interval

@dataclass
class DimensionFilterRequest:
    """Request for filtering by resource labels/dimensions."""
    metric: str
    start: datetime | None = None
    end: datetime | None = None
    **dimensions: str

@dataclass
class DimensionFilterResponse:
    metric: str
    tags: list[str]
    values: list[list[int, float]]

@dataclass
class CompareSeriesRequest:
    metric: str
    start: datetime
    end: datetime
    series_a: dict  # dimension filter dict for first series
    series_b: dict  # dimension filter dict for second series

@dataclass
class CompareSeriesResponse:
    series_a: list[list[int, float]]
    series_b: list[list[int, float]]
