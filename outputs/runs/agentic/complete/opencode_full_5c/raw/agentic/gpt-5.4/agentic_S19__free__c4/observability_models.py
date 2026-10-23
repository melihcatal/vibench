from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def ensure_rfc3339(value: datetime | str) -> str:
    if isinstance(value, str):
        return value
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, dict):
        for key in ("doubleValue", "int64Value"):
            if key in value and value[key] is not None:
                return float(value[key])
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def normalize_labels(labels: Optional[Dict[str, Any]]) -> Dict[str, str]:
    return {str(k): str(v) for k, v in (labels or {}).items() if v is not None}


@dataclass
class MetricWindowRequest:
    project_id: str
    metric_type: str
    start_time: datetime | str
    end_time: datetime | str
    filter_labels: Dict[str, str] = field(default_factory=dict)
    alignment_period_seconds: int = 300
    per_series_aligner: str = "ALIGN_MEAN"
    limit: int = 200

    def interval(self) -> Dict[str, str]:
        return {
            "start_time": ensure_rfc3339(self.start_time),
            "end_time": ensure_rfc3339(self.end_time),
        }


@dataclass
class MetricPoint:
    timestamp: str
    value: Optional[float]
    labels: Dict[str, str] = field(default_factory=dict)
    resource_type: Optional[str] = None
    metric_kind: Optional[str] = None
    value_type: Optional[str] = None
    series_name: Optional[str] = None


@dataclass
class MetricSeriesResponse:
    metric_type: str
    points: List[MetricPoint]
    next_page_token: Optional[str] = None


@dataclass
class AggregatedStats:
    metric_type: str
    statistic: str
    start_time: str
    end_time: str
    value: Optional[float]
    labels: Dict[str, str] = field(default_factory=dict)


@dataclass
class ComparisonResult:
    metric_type: str
    left_label: str
    right_label: str
    left_average: Optional[float]
    right_average: Optional[float]
    delta: Optional[float]
    ratio: Optional[float]


@dataclass
class MetricSummary:
    metric_type: str
    sample_count: int
    average: Optional[float]
    minimum: Optional[float]
    maximum: Optional[float]
    trend: str
    anomaly_detected: bool
