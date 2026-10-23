from __future__ import annotations

import enum
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


class AggregationFunction(enum.Enum):
    AVG = "avg"
    SUM = "sum"
    MIN = "min"
    MAX = "max"
    COUNT = "count"
    RATE = "rate"


class MetricType(enum.Enum):
    GAUGE = "gauge"
    COUNT = "count"
    RATE = "rate"


@dataclass
class MetricQueryRequest:
    metric_name: str
    start: int
    end: int
    interval: Optional[int] = None
    aggregation: Optional[AggregationFunction] = None
    tags: Optional[List[str]] = None
    group_by: Optional[List[str]] = None

    def to_datadog_query(self) -> str:
        tag_filter = ""
        if self.tags:
            tag_filter = "{" + ",".join(self.tags) + "}"
        return f"{self.metric_name}{tag_filter}"

    def to_datadog_params(self) -> Dict[str, Any]:
        params: Dict[str, Any] = {
            "from": self.start,
            "to": self.end,
            "query": self.to_datadog_query(),
        }
        if self.interval:
            params["interval"] = self.interval
        return params


@dataclass
class MetricDataPoint:
    timestamp: int
    value: float
    tags: Optional[Dict[str, str]] = None


@dataclass
class MetricTimeSeries:
    metric_name: str
    scope: str
    points: List[MetricDataPoint] = field(default_factory=list)
    tag_set: Optional[Dict[str, str]] = None
    expression: Optional[str] = None
    unit: Optional[str] = None


@dataclass
class MetricAggregationResult:
    metric_name: str
    query: str
    start: int
    end: int
    aggregation: AggregationFunction
    value: float
    point_count: int = 0
    tag_set: Optional[Dict[str, str]] = None


@dataclass
class MetricComparisonResult:
    series_a: MetricTimeSeries
    series_b: MetricTimeSeries
    diff_values: List[float] = field(default_factory=list)
    diff_percent: List[float] = field(default_factory=list)
    correlation: Optional[float] = None
    mean_diff: Optional[float] = None
    mean_diff_percent: Optional[float] = None
    max_diff: Optional[float] = None
    min_diff: Optional[float] = None


@dataclass
class MetricSummary:
    metric_name: str
    time_window_start: int
    time_window_end: int
    current_value: Optional[float] = None
    previous_value: Optional[float] = None
    trend_direction: Optional[str] = None
    trend_magnitude: Optional[float] = None
    anomaly_detected: bool = False
    anomaly_score: Optional[float] = None
    anomaly_details: Optional[str] = None
    percent_change: Optional[float] = None
    series: Optional[MetricTimeSeries] = None
    summary_text: str = ""


@dataclass
class MetricAnnotation:
    annotation_id: Optional[str] = None
    text: str = ""
    labels: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    timestamp: Optional[int] = None
    source: Optional[str] = None


@dataclass
class AnnotationSafetyResult:
    annotation: MetricAnnotation
    is_safe: bool = True
    safety_score: float = 1.0
    flags: List[str] = field(default_factory=list)
    flag_details: Optional[List[Dict[str, Any]]] = None
    provider: str = ""
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class TranslationResult:
    original_text: str
    translated_text: str
    source_language: str = "auto"
    target_language: str = "en"
    provider: str = ""
    confidence: Optional[float] = None


@dataclass
class MetricExportSnapshot:
    snapshot_id: str
    metric_name: str
    start: int
    end: int
    data: Optional[Dict[str, Any]] = None
    series_list: Optional[List[MetricTimeSeries]] = None
    export_timestamp: Optional[int] = None
    storage_key: Optional[str] = None
    storage_uri: Optional[str] = None
    storage_provider: str = ""


@dataclass
class DashboardNote:
    note_id: Optional[str] = None
    note_text: str = ""
    dashboard_id: Optional[str] = None
    widget_id: Optional[str] = None
    created_at: Optional[int] = None
    updated_at: Optional[int] = None


def normalize_datadog_series(
    raw_series: Dict[str, Any], metric_name: str
) -> MetricTimeSeries:
    scope = raw_series.get("scope", "")
    tag_set = raw_series.get("tag_set", {})
    expression = raw_series.get("expression")
    unit = raw_series.get("unit")

    points = []
    for raw_point in raw_series.get("pointlist", []):
        if len(raw_point) >= 2 and raw_point[1] is not None:
            points.append(
                MetricDataPoint(
                    timestamp=int(raw_point[0] / 1000)
                    if raw_point[0] > 1e12
                    else int(raw_point[0]),
                    value=float(raw_point[1]),
                )
            )

    return MetricTimeSeries(
        metric_name=metric_name,
        scope=scope,
        points=points,
        tag_set=tag_set if tag_set else None,
        expression=expression,
        unit=unit,
    )


def normalize_datadog_v2_series(
    raw_series: Dict[str, Any], metric_name: str
) -> MetricTimeSeries:
    group_tags = {}
    for tag in raw_series.get("group_by", []):
        if isinstance(tag, dict):
            group_tags[tag.get("name", "unknown")] = tag.get("value", "")

    points = []
    for values_list in raw_series.get("values", []):
        if len(values_list) >= 2 and values_list[1] is not None:
            ts_ms = int(values_list[0])
            points.append(
                MetricDataPoint(
                    timestamp=ts_ms // 1000 if ts_ms > 1e12 else ts_ms,
                    value=float(values_list[1]),
                )
            )

    return MetricTimeSeries(
        metric_name=metric_name,
        scope=raw_series.get("scope", ""),
        points=points,
        tag_set=group_tags if group_tags else None,
        expression=raw_series.get("expression"),
        unit=raw_series.get("unit"),
    )


def compute_correlation(xs: List[float], ys: List[float]) -> Optional[float]:
    n = min(len(xs), len(ys))
    if n < 2:
        return None
    xs = xs[:n]
    ys = ys[:n]
    mean_x = sum(xs) / n
    mean_y = sum(ys) / n
    cov = sum((xs[i] - mean_x) * (ys[i] - mean_y) for i in range(n)) / n
    std_x = (sum((x - mean_x) ** 2 for x in xs) / n) ** 0.5
    std_y = (sum((y - mean_y) ** 2 for y in ys) / n) ** 0.5
    if std_x == 0 or std_y == 0:
        return None
    return cov / (std_x * std_y)


def compute_diff_stats(
    values_a: List[float], values_b: List[float]
) -> Dict[str, Optional[float]]:
    n = min(len(values_a), len(values_b))
    if n == 0:
        return {
            "mean_diff": None,
            "mean_diff_percent": None,
            "max_diff": None,
            "min_diff": None,
        }
    diffs = [values_a[i] - values_b[i] for i in range(n)]
    mean_diff = sum(diffs) / n
    max_diff = max(diffs)
    min_diff = min(diffs)
    mean_diff_pct = None
    valid_pcts = []
    for i in range(n):
        if values_b[i] != 0:
            valid_pcts.append((values_a[i] - values_b[i]) / abs(values_b[i]) * 100)
    if valid_pcts:
        mean_diff_pct = sum(valid_pcts) / len(valid_pcts)
    return {
        "mean_diff": mean_diff,
        "mean_diff_percent": mean_diff_pct,
        "max_diff": max_diff,
        "min_diff": min_diff,
    }
