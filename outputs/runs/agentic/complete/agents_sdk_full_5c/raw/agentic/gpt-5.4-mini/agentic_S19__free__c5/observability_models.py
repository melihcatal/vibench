from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Tuple


@dataclass(frozen=True)
class MetricWindowRequest:
    metric_name: str
    start_time: datetime
    end_time: datetime
    dimensions: Mapping[str, str] = field(default_factory=dict)
    statistic: str = "Average"
    period: int = 300


@dataclass(frozen=True)
class MetricPoint:
    timestamp: datetime
    value: float
    unit: Optional[str] = None
    dimensions: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class MetricSeriesResponse:
    metric_name: str
    datapoints: Sequence[MetricPoint]
    label: Optional[str] = None


@dataclass(frozen=True)
class MetricStatisticsResponse:
    metric_name: str
    statistics: Mapping[str, float]
    datapoints: Sequence[MetricPoint] = field(default_factory=tuple)


@dataclass(frozen=True)
class MetricComparisonResponse:
    metric_name: str
    left: MetricSeriesResponse
    right: MetricSeriesResponse
    delta: float


@dataclass(frozen=True)
class MetricSummaryResponse:
    metric_name: str
    summary: str
    trend: str
    anomaly_score: float


@dataclass(frozen=True)
class SafetyCheckResponse:
    text: str
    is_safe: bool
    reason: Optional[str] = None


@dataclass(frozen=True)
class TranslationResponse:
    source_text: str
    target_locale: str
    translated_text: str


@dataclass(frozen=True)
class ExportArchiveResponse:
    bucket: str
    key: str
    etag: Optional[str] = None


def normalize_dimensions(dimensions: Optional[Mapping[str, str]] = None) -> List[Dict[str, str]]:
    if not dimensions:
        return []
    return [{"Name": str(k), "Value": str(v)} for k, v in sorted(dimensions.items())]


def parse_metric_datapoints(raw_datapoints: Iterable[Mapping[str, Any]], metric_name: str, dimensions: Optional[Mapping[str, str]] = None) -> List[MetricPoint]:
    points: List[MetricPoint] = []
    for item in raw_datapoints:
        ts = item.get("Timestamp")
        if isinstance(ts, datetime):
            timestamp = ts.astimezone(timezone.utc)
        else:
            timestamp = datetime.fromisoformat(str(ts).replace("Z", "+00:00")).astimezone(timezone.utc)
        value = float(item.get("Average", item.get("Sum", item.get("Maximum", item.get("Minimum", 0.0)))))
        points.append(
            MetricPoint(
                timestamp=timestamp,
                value=value,
                unit=item.get("Unit"),
                dimensions=dict(dimensions or {}),
            )
        )
    points.sort(key=lambda p: p.timestamp)
    return points
