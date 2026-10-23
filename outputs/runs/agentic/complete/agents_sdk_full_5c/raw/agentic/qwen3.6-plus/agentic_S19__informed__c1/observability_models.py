"""Local request, response, and normalization helpers for Managed Metrics Monitoring.

Defines dataclasses for metric query parameters and response normalization
utilities tailored to Google Cloud Monitoring outputs.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from google.api import distribution_pb2
from google.cloud.monitoring_v3 import TimeInterval


@dataclass
class MetricQueryParams:
    """Normalized query parameters for Google Cloud Monitoring metric requests."""

    metric_name: str
    window_minutes: int = 60
    alignment_period_seconds: int = 60
    per_series_aligner: str = "ALIGN_MEAN"
    resource_type: Optional[str] = "gce_instance"
    labels: Optional[Dict[str, str]] = None
    end_time: Optional[datetime] = None

    def to_time_interval(self) -> TimeInterval:
        """Convert to a Google Cloud Monitoring TimeInterval."""
        end = self.end_time or datetime.utcnow()
        start = end - timedelta(minutes=self.window_minutes)
        interval = TimeInterval()
        interval.end_time.seconds = int(end.timestamp())
        interval.end_time.nanos = int(end.microsecond * 1000)
        interval.start_time.seconds = int(start.timestamp())
        interval.start_time.nanos = int(start.microsecond * 1000)
        return interval


@dataclass
class MetricDataPoint:
    """A single normalized datapoint from a Google Cloud Monitoring series."""

    timestamp: datetime
    value: float
    labels: Dict[str, str] = field(default_factory=dict)


@dataclass
class MetricSeries:
    """A full metric series containing aligned datapoints."""

    metric_type: str
    resource_labels: Dict[str, str] = field(default_factory=dict)
    points: List[MetricDataPoint] = field(default_factory=list)


def normalize_point_value(point_value: Any) -> float:
    """Extract a float from a Google Cloud Monitoring TypedValue."""
    if hasattr(point_value, "double_value"):
        return float(point_value.double_value)
    if hasattr(point_value, "int64_value"):
        return float(point_value.int64_value)
    if hasattr(point_value, "distribution_value"):
        dist: distribution_pb2.Distribution = point_value.distribution_value
        return float(dist.mean) if dist.mean else 0.0
    return 0.0


def build_label_filter(labels: Dict[str, str]) -> str:
    """Build a Google Cloud Monitoring filter string from label key-value pairs."""
    conditions = [
        f'metric.labels.{k} = "{v}"' for k, v in sorted(labels.items())
    ]
    return " AND ".join(conditions)


def compute_series_stats(series: MetricSeries) -> Dict[str, float]:
    """Compute basic aggregation statistics over a normalized metric series."""
    if not series.points:
        return {"count": 0, "min": 0.0, "max": 0.0, "mean": 0.0, "sum": 0.0}
    values = [p.value for p in series.points]
    return {
        "count": len(values),
        "min": min(values),
        "max": max(values),
        "mean": sum(values) / len(values),
        "sum": sum(values),
    }
