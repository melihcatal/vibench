import os
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Optional


class MetricAggregation(Enum):
    AVG = "avg"
    SUM = "sum"
    MIN = "min"
    MAX = "max"
    COUNT = "count"
    P50 = "p50"
    P90 = "p90"
    P95 = "p95"
    P99 = "p99"


class MetricFunction(Enum):
    NONE = "none"
    RATE = "rate"
    ROLLUP = "rollup"
    DIFF = "diff"
    DELTA = "delta"


class MetricType(Enum):
    GAUGE = "gauge"
    COUNT = "count"
    RATE = "rate"


@dataclass
class MetricQueryRequest:
    metric_name: str
    start: datetime
    end: datetime
    aggregation: MetricAggregation = MetricAggregation.AVG
    interval_seconds: int = 60
    dimensions: Optional[dict[str, str]] = None
    function: MetricFunction = MetricFunction.NONE
    rollup_interval: Optional[int] = None

    def to_datadog_query(self) -> str:
        base = f"{self.aggregation.value}:{self.metric_name}"
        if self.dimensions:
            dim_parts = [f"{k}:{v}" for k, v in self.dimensions.items()]
            base = f"{base}{{{{{','.join(dim_parts)}}}}}"
        return base

    def to_datadog_payload(self) -> dict[str, Any]:
        query = self.to_datadog_query()
        payload = {
            "from": int(self.start.timestamp()),
            "to": int(self.end.timestamp()),
            "query": query,
        }
        if self.interval_seconds:
            payload["interval"] = self.interval_seconds
        return payload


@dataclass
class MetricQueryResponse:
    series: list[dict[str, Any]] = field(default_factory=list)
    group_by: list[str] = field(default_factory=list)
    status: str = "ok"
    error: Optional[str] = None

    @property
    def datapoints(self) -> list[tuple[datetime, float]]:
        points = []
        for series in self.series:
            for point in series.get("pointlist", []):
                ts = datetime.fromtimestamp(point[0] / 1000.0)
                value = point[1]
                points.append((ts, value))
        points.sort(key=lambda x: x[0])
        return points

    @property
    def metric_name(self) -> Optional[str]:
        if self.series:
            return self.series[0].get("metric")
        return None

    @property
    def dimensions(self) -> dict[str, str]:
        dims = {}
        for series in self.series:
            scope = series.get("scope", "")
            if scope:
                parts = scope.strip("{}").split(",")
                for part in parts:
                    if ":" in part:
                        k, v = part.split(":", 1)
                        dims[k.strip()] = v.strip()
        return dims


@dataclass
class MetricStatsResult:
    metric_name: str
    aggregation: str
    start: datetime
    end: datetime
    count: int = 0
    avg: float = 0.0
    min_val: float = 0.0
    max_val: float = 0.0
    sum_val: float = 0.0
    p50: float = 0.0
    p90: float = 0.0
    p95: float = 0.0
    p99: float = 0.0
    stddev: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "metric_name": self.metric_name,
            "aggregation": self.aggregation,
            "start": self.start.isoformat(),
            "end": self.end.isoformat(),
            "count": self.count,
            "avg": round(self.avg, 4),
            "min": round(self.min_val, 4),
            "max": round(self.max_val, 4),
            "sum": round(self.sum_val, 4),
            "p50": round(self.p50, 4),
            "p90": round(self.p90, 4),
            "p95": round(self.p95, 4),
            "p99": round(self.p99, 4),
            "stddev": round(self.stddev, 4),
        }


@dataclass
class MetricComparisonResult:
    series_a_name: str
    series_b_name: str
    series_a: list[tuple[datetime, float]] = field(default_factory=list)
    series_b: list[tuple[datetime, float]] = field(default_factory=list)
    correlation: float = 0.0
    mean_diff: float = 0.0
    start: Optional[datetime] = None
    end: Optional[datetime] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "series_a": self.series_a_name,
            "series_b": self.series_b_name,
            "correlation": round(self.correlation, 4),
            "mean_difference": round(self.mean_diff, 4),
            "a_count": len(self.series_a),
            "b_count": len(self.series_b),
            "start": self.start.isoformat() if self.start else None,
            "end": self.end.isoformat() if self.end else None,
        }


@dataclass
class MetricAnomalySummary:
    metric_name: str
    window_start: datetime
    window_end: datetime
    anomalies_detected: int = 0
    anomaly_timestamps: list[datetime] = field(default_factory=list)
    trend_direction: str = "stable"
    trend_slope: float = 0.0
    summary_text: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "metric_name": self.metric_name,
            "window_start": self.window_start.isoformat(),
            "window_end": self.window_end.isoformat(),
            "anomalies_detected": self.anomalies_detected,
            "anomaly_timestamps": [t.isoformat() for t in self.anomaly_timestamps],
            "trend_direction": self.trend_direction,
            "trend_slope": round(self.trend_slope, 6),
            "summary": self.summary_text,
        }


@dataclass
class SafetyCheckResult:
    text: str
    is_safe: bool = True
    categories: dict[str, float] = field(default_factory=dict)
    flagged_categories: list[str] = field(default_factory=list)
    confidence: float = 1.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "is_safe": self.is_safe,
            "flagged_categories": self.flagged_categories,
            "categories": {k: round(v, 4) for k, v in self.categories.items()},
            "confidence": round(self.confidence, 4),
        }


@dataclass
class TranslationResult:
    source_text: str
    translated_text: str
    source_language: str = "en"
    target_language: str = "en"
    confidence: float = 1.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_text": self.source_text,
            "translated_text": self.translated_text,
            "source_language": self.source_language,
            "target_language": self.target_language,
            "confidence": round(self.confidence, 4),
        }


@dataclass
class ArchiveResult:
    key: str
    bucket: str
    size_bytes: int = 0
    etag: Optional[str] = None
    storage_class: str = "STANDARD_IA"
    archived_at: Optional[datetime] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "key": self.key,
            "bucket": self.bucket,
            "size_bytes": self.size_bytes,
            "etag": self.etag,
            "storage_class": self.storage_class,
            "archived_at": self.archived_at.isoformat() if self.archived_at else None,
        }


def normalize_datadog_response(raw_response: dict[str, Any]) -> MetricQueryResponse:
    series = []
    for ts in raw_response.get("series", []):
        series.append(
            {
                "metric": ts.get("metric", ""),
                "scope": ts.get("scope", ""),
                "pointlist": ts.get("pointlist", []),
                "aggr": ts.get("aggr", ""),
                "display_name": ts.get("display_name", ""),
            }
        )
    return MetricQueryResponse(
        series=series,
        status=raw_response.get("status", "ok"),
        error=raw_response.get("error"),
    )


def parse_datadog_error(response: dict[str, Any]) -> Optional[str]:
    if response.get("status") == "error":
        return response.get("error", "Unknown Datadog API error")
    if "errors" in response:
        errors = response["errors"]
        if isinstance(errors, list):
            return "; ".join(str(e) for e in errors)
        return str(errors)
    return None


def build_dimension_filter(dimensions: dict[str, str]) -> str:
    parts = [f"{k}:{v}" for k, v in dimensions.items()]
    return "{" + ",".join(parts) + "}" if parts else ""
