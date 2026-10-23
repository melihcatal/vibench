from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def to_rfc3339(value: datetime | str) -> str:
    if isinstance(value, str):
        return value
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


@dataclass
class MetricWindowRequest:
    metric_type: str
    start_time: datetime | str
    end_time: datetime | str
    project_id: Optional[str] = None
    resource_type: Optional[str] = None
    labels: Dict[str, str] = field(default_factory=dict)
    aligner: str = "ALIGN_MEAN"
    alignment_period_seconds: int = 300

    def to_filter(self) -> str:
        parts = [f'metric.type = "{self.metric_type}"']
        if self.resource_type:
            parts.append(f'resource.type = "{self.resource_type}"')
        for key, value in self.labels.items():
            if key.startswith("metric.labels.") or key.startswith("resource.labels."):
                parts.append(f'{key} = "{value}"')
            else:
                parts.append(f'resource.labels.{key} = "{value}"')
        return " AND ".join(parts)


@dataclass
class MetricPoint:
    timestamp: str
    value: float
    labels: Dict[str, str] = field(default_factory=dict)


@dataclass
class MetricSeries:
    metric_type: str
    resource_type: str
    metric_labels: Dict[str, str]
    resource_labels: Dict[str, str]
    points: List[MetricPoint]


@dataclass
class MetricWindowResponse:
    series: List[MetricSeries]
    next_page_token: Optional[str] = None


@dataclass
class MetricStatsResponse:
    metric_type: str
    start_time: str
    end_time: str
    sample_count: int
    minimum: Optional[float]
    maximum: Optional[float]
    average: Optional[float]
    total: Optional[float]


@dataclass
class MetricComparisonResponse:
    metric_type: str
    start_time: str
    end_time: str
    left_average: Optional[float]
    right_average: Optional[float]
    delta: Optional[float]
    ratio: Optional[float]


def _extract_typed_value(point_value: Any) -> float:
    for key in ("double_value", "int64_value"):
        candidate = getattr(point_value, key, None)
        if candidate is not None:
            return float(candidate)
    distribution = getattr(point_value, "distribution_value", None)
    if distribution is not None:
        mean = getattr(distribution, "mean", None)
        if mean is not None:
            return float(mean)
    bool_value = getattr(point_value, "bool_value", None)
    if bool_value is not None:
        return 1.0 if bool_value else 0.0
    return 0.0


def normalize_time_series(series_list: List[Any]) -> MetricWindowResponse:
    normalized: List[MetricSeries] = []
    for item in series_list:
        points = []
        for point in getattr(item, "points", []):
            interval = getattr(point, "interval", None)
            end_time = getattr(interval, "end_time", None)
            points.append(
                MetricPoint(
                    timestamp=to_rfc3339(end_time) if end_time else "",
                    value=_extract_typed_value(getattr(point, "value", None)),
                    labels=dict(
                        getattr(getattr(item, "metric", None), "labels", {}) or {}
                    ),
                )
            )
        normalized.append(
            MetricSeries(
                metric_type=getattr(getattr(item, "metric", None), "type", ""),
                resource_type=getattr(getattr(item, "resource", None), "type", ""),
                metric_labels=dict(
                    getattr(getattr(item, "metric", None), "labels", {}) or {}
                ),
                resource_labels=dict(
                    getattr(getattr(item, "resource", None), "labels", {}) or {}
                ),
                points=points,
            )
        )
    return MetricWindowResponse(series=normalized)


def flatten_values(response: MetricWindowResponse) -> List[float]:
    values: List[float] = []
    for series in response.series:
        for point in series.points:
            values.append(point.value)
    return values
