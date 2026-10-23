from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass
class MetricWindowRequest:
    metric_name: str
    start_time: datetime
    end_time: datetime
    namespace: str = "AWS/EC2"
    period: int = 300
    statistic: str = "Average"
    dimensions: Dict[str, str] = field(default_factory=dict)
    region_name: Optional[str] = None


@dataclass
class MetricDataPoint:
    timestamp: datetime
    value: float
    unit: Optional[str] = None
    statistic: Optional[str] = None
    source: str = "Amazon CloudWatch"


@dataclass
class MetricSeriesResponse:
    metric_name: str
    namespace: str
    datapoints: List[MetricDataPoint]
    dimensions: Dict[str, str] = field(default_factory=dict)
    label: Optional[str] = None
    source: str = "Amazon CloudWatch"


@dataclass
class AggregateStatsResponse:
    metric_name: str
    namespace: str
    statistics: Dict[str, Optional[float]]
    sample_count: int
    unit: Optional[str] = None
    source: str = "Amazon CloudWatch"


@dataclass
class ComparisonResponse:
    left: MetricSeriesResponse
    right: MetricSeriesResponse
    delta_by_timestamp: List[Dict[str, Any]]
    source: str = "Amazon CloudWatch"



def ensure_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)



def normalize_cloudwatch_datapoints(datapoints: List[Dict[str, Any]], statistic: str) -> List[MetricDataPoint]:
    normalized: List[MetricDataPoint] = []
    for item in sorted(datapoints, key=lambda d: d["Timestamp"]):
        metric_value = item.get(statistic)
        if metric_value is None:
            for candidate in ("Average", "Sum", "Minimum", "Maximum", "SampleCount", "ExtendedStatistics"):
                if candidate in item:
                    metric_value = item[candidate]
                    statistic = candidate
                    break
        if metric_value is None:
            continue
        normalized.append(
            MetricDataPoint(
                timestamp=ensure_utc(item["Timestamp"]),
                value=float(metric_value),
                unit=item.get("Unit"),
                statistic=statistic,
            )
        )
    return normalized



def summarize_points(points: List[MetricDataPoint]) -> Dict[str, Optional[float]]:
    if not points:
        return {"min": None, "max": None, "avg": None, "latest": None}
    values = [point.value for point in points]
    return {
        "min": min(values),
        "max": max(values),
        "avg": sum(values) / len(values),
        "latest": points[-1].value,
    }



def points_to_serializable(points: List[MetricDataPoint]) -> List[Dict[str, Any]]:
    return [
        {
            "timestamp": point.timestamp.isoformat(),
            "value": point.value,
            "unit": point.unit,
            "statistic": point.statistic,
            "source": point.source,
        }
        for point in points
    ]
