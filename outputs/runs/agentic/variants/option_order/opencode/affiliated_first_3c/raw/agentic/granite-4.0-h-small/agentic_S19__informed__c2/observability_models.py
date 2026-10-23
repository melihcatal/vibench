import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class MetricQueryPayload:
    """Payload for querying recent datapoints of a metric."""

    metric: str
    start: int  # Unix timestamp seconds
    end: int  # Unix timestamp seconds
    window: int  # seconds


@dataclass
class MetricAggregatePayload:
    """Payload for retrieving aggregated statistics."""

    metric: str
    start: int
    end: int


@dataclass
class FilterDimensionPayload:
    """Payload for metric data filtered by dimensions."""

    metric: str
    filters: Dict[str, Any]
    start: Optional[int] = None
    end: Optional[int] = None


@dataclass
class CompareSeriesPayload:
    """Payload for comparing metric series between two resources or filters."""

    metric: str
    resourceA: str
    resourceB: str
    filtersA: Dict[str, Any] = None
    filtersB: Dict[str, Any] = None
    start: Optional[int] = None
    end: Optional[int] = None


@dataclass
class MetricResponse:
    """Normalized response structure for metric data."""

    status: str
    data: Any
    message: str = ""

    @classmethod
    def from_raw(cls, raw: Dict[str, Any]) -> "MetricResponse":
        # Normalize different provider structures to a consistent shape
        if "datapoints" in raw:
            return cls(status="ok", data=raw["datapoints"])
        if "statistics" in raw:
            return cls(status="ok", data=raw["statistics"])
        return cls(status="error", data=raw, message=raw.get("message", ""))
