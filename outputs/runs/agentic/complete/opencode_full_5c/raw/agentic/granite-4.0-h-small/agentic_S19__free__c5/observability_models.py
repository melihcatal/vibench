# [HELPER] observability_models.py

# Define local request, response, and normalization helpers for Managed Metrics Monitoring.
# These pure‑Python dataclasses / Pydantic models represent the shape of data passed between
# the scored implementation files and the concrete provider client helper.

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Any, Optional


@dataclass
class MetricQueryRequest:
    """Payload for querying raw datapoints over a time window."""

    metric: str  # e.g., "cpu.usage.percent"
    start: datetime  # inclusive start (timezone-aware)
    end: datetime  # exclusive end (timezone-aware)
    limit: int = 100  # max points to return
    namespace: Optional[str] = None  # optional label scope


@dataclass
class MetricQueryResponse:
    """Normalized response containing raw datapoints and metadata."""

    datapoints: List[Dict[str, Any]]
    metadata: Dict[str, Any]

    @classmethod
    def from_dict(cls, raw: Dict[str, Any]) -> MetricQueryResponse:
        # Example normalization – extract 'timeseries' key.
        datapoints = raw.get("timeseries", [])
        metadata = raw.get("metadata", {})
        return cls(datapoints=datapoints, metadata=metadata)


@dataclass
class MetricStatsRequest:
    """Payload for retrieving aggregated stats (min, max, avg, sum, count)."""

    metric: str
    start: datetime
    end: datetime
    namespace: Optional[str] = None


@dataclass
class MetricStatsResponse:
    """Normalized stats response."""

    min: Optional[float] = None
    max: Optional[float] = None
    avg: Optional[float] = None
    sum: Optional[float] = None
    count: Optional[int] = None

    @classmethod
    def from_dict(cls, raw: Dict[str, Any]) -> MetricStatsResponse:
        # Map common New Relic keys to our fields.
        return cls(
            min=raw.get("min"),
            max=raw.get("max"),
            avg=raw.get("average"),
            sum=raw.get("sum"),
            count=raw.get("count"),
        )


@dataclass
class FilteredMetricRequest:
    """Payload for querying metrics with dimension filters."""

    metric: str
    start: datetime
    end: datetime
    dimensions: Dict[str, List[str]]  # e.g., {'host': ['web-01', 'web-02']}


@dataclass
class FilteredMetricResponse:
    """Normalized filtered metric response."""

    datapoints: List[Dict[str, Any]]
    matched_dimensions: Dict[str, List[str]]

    @classmethod
    def from_dict(cls, raw: Dict[str, Any]) -> FilteredMetricResponse:
        return cls(
            datapoints=raw.get("datapoints", []),
            matched_dimensions=raw.get("matched_dimensions", {}),
        )


@dataclass
class CompareRequest:
    """Payload for comparing two metric series using separate filters."""

    metric: str
    start: datetime
    end: datetime
    left_filter: Dict[str, List[str]]
    right_filter: Dict[str, List[str]]


@dataclass
class CompareResponse:
    """Normalized compare response with side‑by‑side values."""

    left_series: List[float]
    right_series: List[float]
    delta: Optional[float] = None
    pct_change: Optional[float] = None

    @classmethod
    def from_dict(cls, raw: Dict[str, Any]) -> CompareResponse:
        # Assume raw contains two arrays named 'left' and 'right'.
        left_series = raw.get("left", [])
        right_series = raw.get("right", [])
        if left_series and right_series:
            # Simple delta for illustration.
            delta = (
                left_series[-1] - right_series[-1]
                if left_series and right_series
                else None
            )
            pct_change = (
                (delta / left_series[-1] * 100)
                if left_series and left_series[-1]
                else None
            )
        else:
            delta = pct_change = None
        return cls(
            left_series=left_series,
            right_series=right_series,
            delta=delta,
            pct_change=pct_change,
        )


if __name__ == "__main__":
    # Simple sanity checks – demonstrate instantiating models with sample data.
    now = datetime.utcnow()
    start = now - timedelta(minutes=10)
    example_query = MetricQueryRequest(
        metric="disk.usage.percent",
        start=start,
        end=now,
        limit=20,
        namespace="serviceA",
    )
    print("QueryRequest example:", example_query)

    example_stats = MetricStatsResponse(
        min=5.0, max=99.9, avg=47.2, sum=944.0, count=20
    )
    print("StatsResponse example:", example_stats)
