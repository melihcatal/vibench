from dataclasses import dataclass, field
from datetime import datetime
from statistics import mean
from typing import Any, Dict, List, Optional


@dataclass
class MetricWindowRequest:
    metric_name: str
    namespace: str
    start_time: datetime
    end_time: datetime
    period: int
    dimensions: List[Dict[str, str]] = field(default_factory=list)


@dataclass
class MetricDataPoint:
    timestamp: datetime
    average: Optional[float] = None
    minimum: Optional[float] = None
    maximum: Optional[float] = None
    sample_count: Optional[float] = None
    sum: Optional[float] = None


@dataclass
class MetricWindowResponse:
    metric_name: str
    namespace: str
    datapoints: List[MetricDataPoint]
    period: int


@dataclass
class AggregatedMetricStats:
    metric_name: str
    namespace: str
    datapoint_count: int
    average: Optional[float]
    minimum: Optional[float]
    maximum: Optional[float]
    total_sum: Optional[float]


@dataclass
class MetricComparisonResponse:
    metric_name: str
    namespace: str
    left_series: List[MetricDataPoint]
    right_series: List[MetricDataPoint]
    period: int


def _to_dt(value: Any) -> datetime:
    if isinstance(value, datetime):
        return value
    return datetime.fromisoformat(str(value).replace("Z", "+00:00"))


def normalize_datapoints(datapoints: List[Dict[str, Any]]) -> List[MetricDataPoint]:
    items: List[MetricDataPoint] = []
    for dp in sorted(datapoints, key=lambda x: x.get("Timestamp")):
        items.append(
            MetricDataPoint(
                timestamp=_to_dt(dp.get("Timestamp")),
                average=dp.get("Average"),
                minimum=dp.get("Minimum"),
                maximum=dp.get("Maximum"),
                sample_count=dp.get("SampleCount"),
                sum=dp.get("Sum"),
            )
        )
    return items


def summarize_datapoints(metric_name: str, namespace: str, datapoints: List[Dict[str, Any]]) -> AggregatedMetricStats:
    values = normalize_datapoints(datapoints)
    avgs = [d.average for d in values if d.average is not None]
    mins = [d.minimum for d in values if d.minimum is not None]
    maxs = [d.maximum for d in values if d.maximum is not None]
    sums = [d.sum for d in values if d.sum is not None]
    return AggregatedMetricStats(
        metric_name=metric_name,
        namespace=namespace,
        datapoint_count=len(values),
        average=mean(avgs) if avgs else None,
        minimum=min(mins) if mins else None,
        maximum=max(maxs) if maxs else None,
        total_sum=sum(sums) if sums else None,
    )
