from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional


def ensure_utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def isoformat_z(dt: datetime) -> str:
    return ensure_utc(dt).isoformat().replace("+00:00", "Z")


@dataclass
class MetricWindowRequest:
    namespace: str
    metric_name: str
    start_time: datetime
    end_time: datetime
    period: int = 300
    stat: str = "Average"
    dimensions: Dict[str, str] = field(default_factory=dict)


@dataclass
class DimensionFilter:
    name: str
    value: str


@dataclass
class Datapoint:
    timestamp: datetime
    value: Optional[float]
    unit: Optional[str] = None
    dimensions: Dict[str, str] = field(default_factory=dict)
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MetricSeries:
    label: str
    datapoints: List[Datapoint]
    provider: str = "aws_cloudwatch"


@dataclass
class AggregateStats:
    metric_name: str
    start_time: datetime
    end_time: datetime
    sample_count: int
    minimum: Optional[float]
    maximum: Optional[float]
    average: Optional[float]
    sum: Optional[float]
    unit: Optional[str] = None
    provider: str = "aws_cloudwatch"


@dataclass
class ComparisonResult:
    left_label: str
    right_label: str
    left_points: List[Datapoint]
    right_points: List[Datapoint]
    delta_average: Optional[float]
    provider: str = "aws_cloudwatch"


@dataclass
class TrendSummary:
    metric_name: str
    window_start: datetime
    window_end: datetime
    point_count: int
    latest_value: Optional[float]
    average_value: Optional[float]
    direction: str
    anomaly_detected: bool
    provider: str = "aws_bedrock"


@dataclass
class SafetyAssessment:
    text: str
    safe: bool
    category: str
    confidence: float
    provider: str = "openai_moderations"


@dataclass
class TranslationResult:
    source_text: str
    translated_text: str
    target_locale: str
    provider: str = "google_cloud_translate"


@dataclass
class ArchiveResult:
    bucket: str
    key: str
    version_id: Optional[str]
    etag: Optional[str]
    provider: str = "aws_s3"


def normalize_cloudwatch_datapoints(points: Iterable[Dict[str, Any]], stat_key: str) -> List[Datapoint]:
    normalized: List[Datapoint] = []
    for point in sorted(points, key=lambda p: p.get("Timestamp", datetime.min.replace(tzinfo=timezone.utc))):
        ts = point.get("Timestamp")
        if isinstance(ts, datetime):
            ts = ensure_utc(ts)
        normalized.append(
            Datapoint(
                timestamp=ts,
                value=point.get(stat_key),
                unit=point.get("Unit"),
                raw=point,
            )
        )
    return normalized


def average_of_points(points: Iterable[Datapoint]) -> Optional[float]:
    values = [p.value for p in points if p.value is not None]
    if not values:
        return None
    return sum(values) / len(values)
