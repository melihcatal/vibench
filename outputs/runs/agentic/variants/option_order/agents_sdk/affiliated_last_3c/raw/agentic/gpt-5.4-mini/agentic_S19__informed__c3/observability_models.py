from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Iterable, Optional


@dataclass(frozen=True)
class MetricWindowRequest:
    metric_name: str
    start_time: datetime
    end_time: datetime
    namespace: str
    statistic: str = "Average"
    period: int = 300
    dimensions: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True)
class MetricSeriesPoint:
    timestamp: datetime
    value: float


@dataclass(frozen=True)
class MetricSeriesResponse:
    metric_name: str
    namespace: str
    datapoints: tuple[MetricSeriesPoint, ...]


@dataclass(frozen=True)
class MetricStatsResponse:
    metric_name: str
    namespace: str
    minimum: float | None
    maximum: float | None
    average: float | None
    sum: float | None
    sample_count: float | None


@dataclass(frozen=True)
class MetricComparisonResponse:
    metric_name: str
    left: MetricSeriesResponse
    right: MetricSeriesResponse


@dataclass(frozen=True)
class NormalizedMetricPoint:
    timestamp: datetime
    value: float
    dimensions: tuple[tuple[str, str], ...] = ()


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def dimensions_to_list(dimensions: Iterable[tuple[str, str]]) -> list[dict[str, str]]:
    return [{"Name": name, "Value": value} for name, value in dimensions]


def normalize_datapoints(datapoints: Iterable[dict[str, Any]]) -> tuple[MetricSeriesPoint, ...]:
    ordered = sorted(datapoints, key=lambda item: item["Timestamp"])
    return tuple(MetricSeriesPoint(timestamp=item["Timestamp"], value=float(item.get("Average", item.get("Value", 0.0)))) for item in ordered)
