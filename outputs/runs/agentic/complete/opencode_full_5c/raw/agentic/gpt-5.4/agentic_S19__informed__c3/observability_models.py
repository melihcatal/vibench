from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Mapping, Optional


def ensure_utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def to_epoch_seconds(dt: datetime) -> int:
    return int(ensure_utc(dt).timestamp())


def isoformat_utc(dt: datetime) -> str:
    return ensure_utc(dt).isoformat()


def normalize_dimensions(
    dimensions: Optional[Mapping[str, Any]] = None,
) -> Dict[str, str]:
    if not dimensions:
        return {}
    normalized: Dict[str, str] = {}
    for key, value in dimensions.items():
        if value is None:
            continue
        normalized[str(key)] = str(value)
    return normalized


def dimensions_to_cloudwatch(
    dimensions: Optional[Mapping[str, Any]] = None,
) -> List[Dict[str, str]]:
    return [
        {"Name": key, "Value": value}
        for key, value in normalize_dimensions(dimensions).items()
    ]


@dataclass
class MetricWindowRequest:
    namespace: str
    metric_name: str
    start_time: datetime
    end_time: datetime
    period: int = 60
    stat: str = "Average"
    unit: Optional[str] = None
    dimensions: Dict[str, str] = field(default_factory=dict)

    def cloudwatch_dimensions(self) -> List[Dict[str, str]]:
        return dimensions_to_cloudwatch(self.dimensions)


@dataclass
class Datapoint:
    timestamp: str
    value: float
    unit: Optional[str] = None
    stat: Optional[str] = None
    dimensions: Dict[str, str] = field(default_factory=dict)


@dataclass
class MetricSeriesResponse:
    provider: str
    namespace: str
    metric_name: str
    start_time: str
    end_time: str
    period: int
    stat: str
    datapoints: List[Datapoint]


@dataclass
class AggregateStatsResponse:
    provider: str
    namespace: str
    metric_name: str
    start_time: str
    end_time: str
    sample_count: int
    minimum: Optional[float]
    maximum: Optional[float]
    average: Optional[float]
    sum: Optional[float]
    unit: Optional[str]
    dimensions: Dict[str, str] = field(default_factory=dict)


@dataclass
class ComparisonResponse:
    provider: str
    metric_name: str
    left_dimensions: Dict[str, str]
    right_dimensions: Dict[str, str]
    left_latest: Optional[float]
    right_latest: Optional[float]
    delta: Optional[float]
    ratio: Optional[float]
    left_points: List[Datapoint]
    right_points: List[Datapoint]


def normalize_cloudwatch_datapoints(
    datapoints: List[Mapping[str, Any]],
    stat: str,
    dimensions: Optional[Mapping[str, Any]] = None,
) -> List[Datapoint]:
    dim_map = normalize_dimensions(dimensions)
    normalized: List[Datapoint] = []
    stat_key = stat[0].upper() + stat[1:]
    for item in sorted(datapoints, key=lambda entry: entry["Timestamp"]):
        value = item.get(stat_key)
        if value is None:
            continue
        normalized.append(
            Datapoint(
                timestamp=isoformat_utc(item["Timestamp"]),
                value=float(value),
                unit=item.get("Unit"),
                stat=stat_key,
                dimensions=dict(dim_map),
            )
        )
    return normalized
