"""Local request, response, and normalization helpers for Managed Metrics Monitoring.

Provides data models for metric queries, aggregation results, dimension filters,
and response normalization utilities that wrap Google Cloud Monitoring types.
"""

from __future__ import annotations

import dataclasses
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class AggregationKind(str, Enum):
    """Supported aggregation kinds aligned with Google Cloud Monitoring."""

    AVERAGE = "AGGREGATION_MEAN"
    COUNT = "AGGREGATION_COUNT"
    SUM = "AGGREGATION_SUM"
    MIN = "AGGREGATION_MIN"
    MAX = "AGGREGATION_MAX"
    STDDEV = "AGGREGATION_STDDEV"
    PERCENTILE_50 = "AGGREGATION_PERCENTILE_05"
    PERCENTILE_95 = "AGGREGATION_PERCENTILE_95"
    PERCENTILE_99 = "AGGREGATION_PERCENTILE_99"


class AlignmentPeriod(str, Enum):
    """Common alignment periods for metric aggregation."""

    ONE_MINUTE = "60s"
    FIVE_MINUTES = "300s"
    FIFTEEN_MINUTES = "900s"
    ONE_HOUR = "3600s"
    ONE_DAY = "86400s"


@dataclasses.dataclass
class MetricQueryRequest:
    """Request model for querying metric datapoints.

    Attributes correspond to Google Cloud Monitoring list_time_series parameters.
    """

    metric_type: str
    project_id: str
    start_time: datetime
    end_time: datetime
    filter_expression: Optional[str] = None
    aggregation_kind: Optional[AggregationKind] = None
    alignment_period: Optional[AlignmentPeriod] = None
    per_series_aligner: Optional[str] = None

    def to_gcm_filter(self) -> str:
        """Build Google Cloud Monitoring filter string."""
        base = f'metric.type = "{self.metric_type}"'
        if self.filter_expression:
            base = f'{base} AND {self.filter_expression}'
        return base

    def to_gcm_interval(self) -> dict:
        """Build Google Cloud Monitoring TimeInterval dict."""
        return {
            "start_time": self.start_time.isoformat() + "Z",
            "end_time": self.end_time.isoformat() + "Z",
        }


@dataclasses.dataclass
class MetricDataPoint:
    """Normalized single datapoint from a metric time series."""

    timestamp: datetime
    value: float
    labels: Dict[str, str] = dataclasses.field(default_factory=dict)
    metric_kind: str = ""
    unit: str = ""


@dataclasses.dataclass
class MetricSeries:
    """A single metric time series with its metadata and points."""

    metric_type: str
    resource_type: str
    resource_labels: Dict[str, str] = dataclasses.field(default_factory=dict)
    metric_labels: Dict[str, str] = dataclasses.field(default_factory=dict)
    points: List[MetricDataPoint] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class AggregationResult:
    """Result of aggregated metric statistics."""

    metric_type: str
    aggregation: AggregationKind
    alignment_period: AlignmentPeriod
    series: List[MetricSeries]
    summary: Dict[str, float] = dataclasses.field(default_factory=dict)


@dataclasses.dataclass
class DimensionFilter:
    """Filter specification for metric dimensions / resource labels."""

    dimension_name: str
    operator: str  # "=", "!=", "=~", "!=~"
    value: str

    def to_gcm_fragment(self) -> str:
        """Convert to Google Cloud Monitoring filter fragment."""
        if self.operator == "=":
            return f'{self.dimension_name} = "{self.value}"'
        elif self.operator == "!=":
            return f'{self.dimension_name} != "{self.value}"'
        elif self.operator == "=~":
            return f'{self.dimension_name} =~ "{self.value}"'
        elif self.operator == "!=~":
            return f'{self.dimension_name} !=~ "{self.value}"'
        else:
            return f'{self.dimension_name} {self.operator} "{self.value}"'


@dataclasses.dataclass
class MetricComparisonResult:
    """Result of comparing two metric series."""

    series_a: MetricSeries
    series_b: MetricSeries
    delta_mean: float
    delta_max: float
    delta_min: float
    correlation: Optional[float] = None


def normalize_gcm_point(gcm_point: dict, metric_labels: Dict[str, str] = None) -> MetricDataPoint:
    """Normalize a Google Cloud Monitoring point dict into a MetricDataPoint."""
    from google.protobuf.timestamp_pb2 import Timestamp

    ts = gcm_point.get("interval", {}).get("end_time", gcm_point.get("interval", {}).get("start_time", ""))
    if ts.endswith("Z"):
        ts = ts[:-1] + "+00:00"

    value_obj = gcm_point.get("value", {})
    value = (
        value_obj.get("double_value")
        or value_obj.get("int64_value", 0)
        or value_obj.get("bool_value", False)
    )
    if isinstance(value, bool):
        value = 1.0 if value else 0.0

    return MetricDataPoint(
        timestamp=datetime.fromisoformat(ts),
        value=float(value),
        labels=metric_labels or {},
        metric_kind=gcm_point.get("metric_kind", ""),
        unit=gcm_point.get("unit", ""),
    )


def normalize_gcm_series(gcm_series: dict) -> MetricSeries:
    """Normalize a Google Cloud Monitoring TimeSeries into a MetricSeries."""
    metric_info = gcm_series.get("metric", {})
    resource_info = gcm_series.get("resource", {})

    metric_labels = metric_info.get("labels", {})
    points = [normalize_gcm_point(p, metric_labels) for p in gcm_series.get("points", [])]

    return MetricSeries(
        metric_type=metric_info.get("type", ""),
        resource_type=resource_info.get("type", ""),
        resource_labels=resource_info.get("labels", {}),
        metric_labels=metric_labels,
        points=points,
    )


def build_aggregation_dict(
    aggregation: AggregationKind,
    alignment_period: AlignmentPeriod,
    per_series_aligner: Optional[str] = None,
) -> dict:
    """Build aggregation dict for Google Cloud Monitoring list_time_series request."""
    aligner = per_series_aligner or aggregation.value
    return {
        "alignment_period": alignment_period.value,
        "per_series_aligner": aligner,
    }
