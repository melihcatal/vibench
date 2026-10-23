from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from datetime import datetime
import enum


class MetricKind(enum.Enum):
    GAUGE = "GAUGE"
    DELTA = "DELTA"
    CUMULATIVE = "CUMULATIVE"


class ValueType(enum.Enum):
    DOUBLE = "DOUBLE"
    INT64 = "INT64"
    DISTRIBUTION = "DISTRIBUTION"
    BOOL = "BOOL"
    STRING = "STRING"


@dataclass
class MetricPoint:
    timestamp: datetime
    value: Any

    def to_dict(self):
        return {"timestamp": self.timestamp.isoformat(), "value": self.value}


@dataclass
class TimeSeriesData:
    metric_labels: Dict[str, str]
    resource_labels: Dict[str, str]
    metric_kind: MetricKind
    value_type: ValueType
    points: List[MetricPoint]

    def to_dict(self):
        return {
            "metric": self.metric_labels,
            "resource": self.resource_labels,
            "metric_kind": self.metric_kind.value,
            "value_type": self.value_type.value,
            "points": [p.to_dict() for p in self.points],
        }


@dataclass
class MetricQueryRequest:
    metric_type: str
    start_minutes: int
    end_minutes: int = 0
    filter_str: Optional[str] = None
    aggregation: Optional[str] = None
    alignment_period: Optional[str] = None

    def to_filter_string(self):
        from observability_client import ObservabilityClient

        client = ObservabilityClient()
        return client.build_time_series_filter(self.metric_type, self.filter_str)


@dataclass
class MetricAggregationResult:
    series_count: int
    total_points: int
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    avg_value: Optional[float] = None
    sum_value: Optional[float] = None
    percentiles: Dict[str, float] = None

    def to_dict(self):
        result = {"series_count": self.series_count, "total_points": self.total_points}
        if self.min_value is not None:
            result["min"] = self.min_value
        if self.max_value is not None:
            result["max"] = self.max_value
        if self.avg_value is not None:
            result["avg"] = self.avg_value
        if self.sum_value is not None:
            result["sum"] = self.sum_value
        if self.percentiles:
            result["percentiles"] = self.percentiles
        return result


@dataclass
class MetricComparisonResult:
    series_a: List[TimeSeriesData]
    series_b: List[TimeSeriesData]
    comparison_metrics: Dict[str, Any]

    def to_dict(self):
        return {
            "series_a": [s.to_dict() for s in self.series_a],
            "series_b": [s.to_dict() for s in self.series_b],
            "comparison": self.comparison_metrics,
        }


def normalize_google_metric_type(metric_type: str) -> str:
    if not metric_type.startswith("custom.googleapis.com/"):
        return metric_type
    return metric_type.replace("custom.googleapis.com/", "")


def build_dimension_filter(dimensions: Dict[str, str]) -> str:
    filters = []
    for key, value in dimensions.items():
        filters.append(f'resource.labels.{key} = "{value}"')
    return " AND ".join(filters)


def parse_aggregation_response(
    response_data: List[Dict[str, Any]],
) -> MetricAggregationResult:
    if not response_data:
        return MetricAggregationResult(series_count=0, total_points=0)

    all_values = []
    for series in response_data:
        for point in series.get("points", []):
            value = point.get("value")
            if isinstance(value, (int, float)):
                all_values.append(value)

    if not all_values:
        return MetricAggregationResult(
            series_count=len(response_data),
            total_points=sum(len(s.get("points", [])) for s in response_data),
        )

    return MetricAggregationResult(
        series_count=len(response_data),
        total_points=len(all_values),
        min_value=min(all_values),
        max_value=max(all_values),
        avg_value=sum(all_values) / len(all_values),
        sum_value=sum(all_values),
    )
