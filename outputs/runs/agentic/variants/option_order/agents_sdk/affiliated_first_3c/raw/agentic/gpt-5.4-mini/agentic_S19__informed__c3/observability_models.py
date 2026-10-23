from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, Optional


@dataclass(frozen=True)
class MetricQuery:
    metric_name: str
    start_time: datetime
    end_time: datetime
    period_seconds: int = 60
    namespace: Optional[str] = None
    dimensions: Dict[str, str] = field(default_factory=dict)
    statistics: List[str] = field(default_factory=lambda: ["Average"])
    unit: Optional[str] = None

    def validated(self) -> "MetricQuery":
        if self.start_time.tzinfo is None:
            object.__setattr__(self, "start_time", self.start_time.replace(tzinfo=timezone.utc))
        if self.end_time.tzinfo is None:
            object.__setattr__(self, "end_time", self.end_time.replace(tzinfo=timezone.utc))
        return self


@dataclass(frozen=True)
class MetricPoint:
    timestamp: datetime
    value: float
    statistic: str = "Average"


@dataclass(frozen=True)
class MetricQueryResult:
    raw: Mapping[str, Any]
    points: List[MetricPoint]


@dataclass(frozen=True)
class MetricSummary:
    metric_name: str
    average: float
    minimum: float
    maximum: float
    count: int
    anomaly_score: float


@dataclass(frozen=True)
class TranslationRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None


@dataclass(frozen=True)
class ArchivedObjectRef:
    bucket: str
    key: str
    etag: Optional[str] = None


def normalize_series_points(raw_points: Iterable[Mapping[str, Any]]) -> List[MetricPoint]:
    points: List[MetricPoint] = []
    for point in raw_points:
        timestamp = point.get("Timestamp") or point.get("timestamp")
        value = point.get("Average")
        if value is None:
            value = point.get("Sum")
        if value is None:
            value = point.get("Maximum")
        if value is None:
            value = point.get("Minimum")
        if timestamp is None or value is None:
            continue
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        points.append(MetricPoint(timestamp=timestamp, value=float(value)))
    points.sort(key=lambda p: p.timestamp)
    return points
