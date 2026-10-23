from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum


class MetricValueType(Enum):
    DOUBLE = "DOUBLE"
    INT64 = "INT64"
    DISTRIBUTION = "DISTRIBUTION"
    STRING = "STRING"
    BOOL = "BOOL"


class AggregationAligner(Enum):
    ALIGN_NONE = "ALIGN_NONE"
    ALIGN_DELTA = "ALIGN_DELTA"
    ALIGN_RATE = "ALIGN_RATE"
    ALIGN_INTERPOLATE = "ALIGN_INTERPOLATE"
    ALIGN_NEXT_OLDER = "ALIGN_NEXT_OLDER"
    ALIGN_MIN = "ALIGN_MIN"
    ALIGN_MAX = "ALIGN_MAX"
    ALIGN_MEAN = "ALIGN_MEAN"
    ALIGN_COUNT = "ALIGN_COUNT"
    ALIGN_SUM = "ALIGN_SUM"
    ALIGN_STDDEV = "ALIGN_STDDEV"
    ALIGN_COUNT_TRUE = "ALIGN_COUNT_TRUE"
    ALIGN_FRACTION_TRUE = "ALIGN_FRACTION_TRUE"
    ALIGN_PERCENTILE_99 = "ALIGN_PERCENTILE_99"
    ALIGN_PERCENTILE_95 = "ALIGN_PERCENTILE_95"
    ALIGN_PERCENTILE_50 = "ALIGN_PERCENTILE_50"
    ALIGN_PERCENTILE_05 = "ALIGN_PERCENTILE_05"


@dataclass
class MetricPoint:
    timestamp: datetime
    value: float
    raw_value: Any = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "value": self.value,
            "raw_value": self.raw_value,
        }


@dataclass
class TimeSeries:
    metric_type: str
    metric_labels: Dict[str, str] = field(default_factory=dict)
    resource_type: str = ""
    resource_labels: Dict[str, str] = field(default_factory=dict)
    value_type: MetricValueType = MetricValueType.DOUBLE
    points: List[MetricPoint] = field(default_factory=list)

    def add_point(self, point: MetricPoint):
        self.points.append(point)

    def get_statistics(self) -> Dict[str, float]:
        if not self.points:
            return {}

        values = [p.value for p in self.points]
        return {
            "mean": sum(values) / len(values),
            "min": min(values),
            "max": max(values),
            "count": len(values),
            "sum": sum(values),
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "metric_type": self.metric_type,
            "metric_labels": self.metric_labels,
            "resource_type": self.resource_type,
            "resource_labels": self.resource_labels,
            "value_type": self.value_type.value,
            "points": [p.to_dict() for p in self.points],
            "statistics": self.get_statistics(),
        }


@dataclass
class MetricQueryRequest:
    metric_type: str
    start_time: datetime
    end_time: datetime
    filters: Dict[str, str] = field(default_factory=dict)
    aggregation_alignment_minutes: Optional[int] = None
    per_series_aligner: AggregationAligner = AggregationAligner.ALIGN_MEAN

    def validate(self):
        if self.start_time >= self.end_time:
            raise ValueError("start_time must be before end_time")
        if not self.metric_type:
            raise ValueError("metric_type is required")


@dataclass
class MetricQueryResponse:
    request: MetricQueryRequest
    time_series: List[TimeSeries] = field(default_factory=list)
    query_execution_time: Optional[datetime] = None
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "request": {
                "metric_type": self.request.metric_type,
                "start_time": self.request.start_time.isoformat(),
                "end_time": self.request.end_time.isoformat(),
                "filters": self.request.filters,
            },
            "time_series": [ts.to_dict() for ts in self.time_series],
            "query_execution_time": self.query_execution_time.isoformat()
            if self.query_execution_time
            else None,
            "error": self.error,
            "total_series": len(self.time_series),
            "total_points": sum(len(ts.points) for ts in self.time_series),
        }


@dataclass
class MetricComparison:
    metric_type: str
    series_a: TimeSeries
    series_b: TimeSeries
    comparison_metrics: Dict[str, float] = field(default_factory=dict)

    def calculate_comparison(self):
        stats_a = self.series_a.get_statistics()
        stats_b = self.series_b.get_statistics()

        if not stats_a or not stats_b:
            return

        self.comparison_metrics = {
            "mean_difference": stats_b["mean"] - stats_a["mean"],
            "percent_difference": (
                (stats_b["mean"] - stats_a["mean"]) / stats_a["mean"] * 100
            )
            if stats_a["mean"] != 0
            else float("inf"),
            "min_difference": stats_b["min"] - stats_a["min"],
            "max_difference": stats_b["max"] - stats_a["max"],
            "relative_variance": (stats_b["max"] - stats_b["min"])
            / (stats_a["max"] - stats_a["min"])
            if (stats_a["max"] - stats_a["min"]) != 0
            else float("inf"),
        }
