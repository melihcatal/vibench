from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from statistics import mean
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

from google.protobuf import timestamp_pb2


@dataclass(frozen=True)
class MetricWindowRequest:
    metric_type: str
    minutes: int = 60
    filter_expression: str = ""
    resource_type: str = ""
    aligner: str = "ALIGN_MEAN"


@dataclass(frozen=True)
class MetricAggregationRequest:
    metric_type: str
    minutes: int = 60
    aligner: str = "ALIGN_MEAN"
    reducer: str = "REDUCE_MEAN"
    group_by_fields: Sequence[str] = field(default_factory=tuple)
    filter_expression: str = ""


@dataclass(frozen=True)
class MetricDimensionFilterRequest:
    metric_type: str
    minutes: int = 60
    filter_expression: str = ""
    labels: Dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class MetricCompareRequest:
    metric_type: str
    minutes: int = 60
    left_filter: str = ""
    right_filter: str = ""


@dataclass(frozen=True)
class MetricSummaryRequest:
    metric_type: str
    minutes: int = 180
    filter_expression: str = ""


@dataclass(frozen=True)
class AnnotationSafetyRequest:
    text: str


@dataclass(frozen=True)
class DashboardNoteTranslateRequest:
    text: str
    target_language_code: str


@dataclass(frozen=True)
class MetricsExportArchiveRequest:
    metric_type: str
    minutes: int = 60
    destination_blob_name: str = ""


@dataclass
class MetricPoint:
    timestamp: datetime
    value: float
    labels: Dict[str, str] = field(default_factory=dict)


@dataclass
class MetricSeries:
    metric_type: str
    points: List[MetricPoint] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def values(self) -> List[float]:
        return [point.value for point in self.points]

    def mean_value(self) -> Optional[float]:
        vals = self.values()
        return mean(vals) if vals else None

    def min_value(self) -> Optional[float]:
        vals = self.values()
        return min(vals) if vals else None

    def max_value(self) -> Optional[float]:
        vals = self.values()
        return max(vals) if vals else None


@dataclass(frozen=True)
class OperationResult:
    ok: bool
    message: str
    payload: Dict[str, Any] = field(default_factory=dict)


def to_timestamp(dt: datetime) -> timestamp_pb2.Timestamp:
    ts = timestamp_pb2.Timestamp()
    ts.FromDatetime(dt)
    return ts


def normalize_points(points: Iterable[Any]) -> List[MetricPoint]:
    normalized: List[MetricPoint] = []
    for item in points:
        if isinstance(item, MetricPoint):
            normalized.append(item)
            continue
        timestamp = getattr(item, "timestamp", None) or getattr(item, "time", None)
        value = getattr(item, "value", None)
        labels = dict(getattr(item, "labels", {}) or {})
        if timestamp is None or value is None:
            continue
        normalized.append(MetricPoint(timestamp=timestamp, value=float(value), labels=labels))
    return normalized


def summarize_series(series: MetricSeries) -> Dict[str, Any]:
    values = series.values()
    return {
        "metric_type": series.metric_type,
        "count": len(values),
        "mean": series.mean_value(),
        "min": series.min_value(),
        "max": series.max_value(),
        "points": [
            {"timestamp": point.timestamp.isoformat(), "value": point.value, "labels": point.labels}
            for point in series.points
        ],
    }
