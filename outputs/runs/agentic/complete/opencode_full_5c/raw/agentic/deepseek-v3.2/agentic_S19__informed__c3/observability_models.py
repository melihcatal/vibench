from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class MetricQueryRequest:
    metric_name: str
    start_minutes_ago: int
    end_minutes_ago: int
    dimension_filters: Optional[Dict[str, str]] = None
    aggregation_period: Optional[int] = None
    aggregation_aligner: Optional[str] = None

    def validate(self):
        if self.start_minutes_ago <= 0 or self.end_minutes_ago <= 0:
            raise ValueError("Time window must be positive")
        if self.start_minutes_ago <= self.end_minutes_ago:
            raise ValueError("start_minutes_ago must be greater than end_minutes_ago")
        return True


@dataclass
class MetricDataPoint:
    timestamp: datetime
    value: float
    metric_type: str
    labels: Dict[str, str]
    resource_labels: Dict[str, str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "value": self.value,
            "metric_type": self.metric_type,
            "labels": self.labels,
            "resource_labels": self.resource_labels,
        }


@dataclass
class MetricAggregationResult:
    count: int
    sum: float
    mean: float
    min: float
    max: float
    std_dev: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "count": self.count,
            "sum": self.sum,
            "mean": self.mean,
            "min": self.min,
            "max": self.max,
        }
        if self.std_dev is not None:
            result["std_dev"] = self.std_dev
        return result


@dataclass
class MetricComparisonResult:
    series_a_stats: MetricAggregationResult
    series_b_stats: MetricAggregationResult
    difference: Dict[str, float]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "series_a": self.series_a_stats.to_dict(),
            "series_b": self.series_b_stats.to_dict(),
            "difference": self.difference,
        }


@dataclass
class TimeWindow:
    start: datetime
    end: datetime

    @classmethod
    def from_minutes_ago(cls, start_minutes_ago: int, end_minutes_ago: int):
        from datetime import datetime, timedelta

        now = datetime.utcnow()
        return cls(
            start=now - timedelta(minutes=start_minutes_ago),
            end=now - timedelta(minutes=end_minutes_ago),
        )


def normalize_google_monitoring_response(time_series_data) -> List[MetricDataPoint]:
    points = []
    for ts in time_series_data:
        for point in ts.points:
            if point.value.HasField("double_value"):
                value = point.value.double_value
            elif point.value.HasField("int64_value"):
                value = float(point.value.int64_value)
            else:
                continue

            data_point = MetricDataPoint(
                timestamp=point.interval.end_time.ToDatetime(),
                value=value,
                metric_type=ts.metric.type,
                labels=dict(ts.metric.labels),
                resource_labels=dict(ts.resource.labels) if ts.resource.labels else {},
            )
            points.append(data_point)
    return points


def calculate_aggregation_stats(
    points: List[MetricDataPoint],
) -> MetricAggregationResult:
    if not points:
        return MetricAggregationResult(count=0, sum=0.0, mean=0.0, min=0.0, max=0.0)

    values = [p.value for p in points]
    count = len(values)
    total = sum(values)
    mean = total / count
    min_val = min(values)
    max_val = max(values)

    if count > 1:
        variance = sum((x - mean) ** 2 for x in values) / (count - 1)
        std_dev = variance**0.5
        return MetricAggregationResult(
            count=count, sum=total, mean=mean, min=min_val, max=max_val, std_dev=std_dev
        )
    else:
        return MetricAggregationResult(
            count=count, sum=total, mean=mean, min=min_val, max=max_val
        )
