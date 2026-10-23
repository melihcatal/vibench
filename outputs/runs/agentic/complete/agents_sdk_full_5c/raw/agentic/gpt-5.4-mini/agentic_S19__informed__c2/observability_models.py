from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def isoformat(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_datetime(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    return datetime.fromisoformat(value)


@dataclass
class MetricQuery:
    metric_name: str
    start_time: datetime
    end_time: datetime
    dimensions: Dict[str, str] = field(default_factory=dict)
    granularity: Optional[int] = None

    def normalized_dimensions(self) -> Dict[str, str]:
        return {str(k): str(v) for k, v in sorted(self.dimensions.items())}


@dataclass
class MetricDatapoint:
    timestamp: datetime
    value: float
    dimensions: Dict[str, str] = field(default_factory=dict)


@dataclass
class MetricSeries:
    metric_name: str
    datapoints: List[MetricDatapoint] = field(default_factory=list)
    dimensions: Dict[str, str] = field(default_factory=dict)


@dataclass
class MetricStats:
    metric_name: str
    start_time: datetime
    end_time: datetime
    minimum: Optional[float] = None
    maximum: Optional[float] = None
    average: Optional[float] = None
    sum: Optional[float] = None
    count: Optional[int] = None


@dataclass
class MetricComparison:
    metric_name: str
    left: MetricSeries
    right: MetricSeries
    delta_average: Optional[float] = None


@dataclass
class MetricSummary:
    metric_name: str
    start_time: datetime
    end_time: datetime
    trend: str
    anomaly_score: Optional[float] = None
    note: Optional[str] = None


@dataclass
class SafetyResult:
    text: str
    provider: str
    unsafe: bool
    labels: Dict[str, float] = field(default_factory=dict)
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranslationResult:
    source_text: str
    translated_text: str
    source_locale: str
    target_locale: str
    provider: str


@dataclass
class ExportArchiveResult:
    bucket: str
    key: str
    etag: Optional[str] = None
    uri: Optional[str] = None


def normalize_points(points: Iterable[Mapping[str, Any]]) -> List[MetricDatapoint]:
    normalized: List[MetricDatapoint] = []
    for point in points:
        ts = point.get("timestamp") or point.get("time") or point.get("datetime")
        value = point.get("value") or point.get("avg") or point.get("sum")
        dims = point.get("dimensions") or point.get("tags") or {}
        if isinstance(ts, str):
            ts = parse_datetime(ts)
        if ts is None:
            continue
        normalized.append(MetricDatapoint(timestamp=ts, value=float(value), dimensions=dict(dims)))
    return normalized


def window_from_minutes(minutes: int) -> tuple[datetime, datetime]:
    end = utc_now()
    start = end - timedelta(minutes=minutes)
    return start, end
