from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass
class MetricQueryWindow:
    namespace: str
    metric_name: str
    start_time: datetime
    end_time: datetime
    period: int = 60
    stat: str = "Average"
    unit: Optional[str] = None
    dimensions: Dict[str, str] = field(default_factory=dict)

    def to_cloudwatch_dimensions(self) -> List[Dict[str, str]]:
        return [{"Name": key, "Value": value} for key, value in sorted(self.dimensions.items())]


@dataclass
class MetricDatapoint:
    timestamp: str
    value: float
    unit: Optional[str] = None
    stat: Optional[str] = None
    dimensions: Dict[str, str] = field(default_factory=dict)


@dataclass
class MetricSeriesResponse:
    metric_name: str
    namespace: str
    start_time: str
    end_time: str
    period: int
    stat: str
    datapoints: List[MetricDatapoint]

    def to_dict(self) -> Dict[str, Any]:
        payload = asdict(self)
        payload["datapoints"] = [asdict(point) for point in self.datapoints]
        return payload


@dataclass
class AggregatedMetricStats:
    metric_name: str
    namespace: str
    stat: str
    sample_count: int
    minimum: Optional[float]
    maximum: Optional[float]
    average: Optional[float]
    sum: Optional[float]
    unit: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class MetricComparison:
    metric_name: str
    namespace: str
    left_filter: Dict[str, str]
    right_filter: Dict[str, str]
    left_average: Optional[float]
    right_average: Optional[float]
    delta: Optional[float]
    ratio: Optional[float]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class MetricSummaryResult:
    summary_text: str
    trend: str
    anomaly_flag: bool
    datapoint_count: int

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SafetyCheckResult:
    text: str
    unsafe: bool
    scores: Dict[str, float]
    blocked_categories: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class TranslationResult:
    source_text: str
    translated_text: str
    target_language: str
    detected_source_language: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ArchiveResult:
    bucket: str
    object_name: str
    uri: str
    md5_hash: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def to_rfc3339(value: datetime) -> str:
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc).isoformat()


def normalize_cloudwatch_datapoints(
    metric_name: str,
    namespace: str,
    start_time: datetime,
    end_time: datetime,
    period: int,
    stat: str,
    dimensions: Dict[str, str],
    datapoints: List[Dict[str, Any]],
) -> MetricSeriesResponse:
    normalized: List[MetricDatapoint] = []
    for item in sorted(datapoints, key=lambda d: d.get("Timestamp")):
        stat_value = item.get(stat)
        if stat_value is None:
            candidates = [item.get("Average"), item.get("Sum"), item.get("Maximum"), item.get("Minimum")]
            stat_value = next((v for v in candidates if v is not None), None)
        if stat_value is None:
            continue
        timestamp = item["Timestamp"]
        normalized.append(
            MetricDatapoint(
                timestamp=to_rfc3339(timestamp),
                value=float(stat_value),
                unit=item.get("Unit"),
                stat=stat,
                dimensions=dict(dimensions),
            )
        )
    return MetricSeriesResponse(
        metric_name=metric_name,
        namespace=namespace,
        start_time=to_rfc3339(start_time),
        end_time=to_rfc3339(end_time),
        period=period,
        stat=stat,
        datapoints=normalized,
    )
