from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any, Mapping, Optional


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(slots=True)
class MetricWindow:
    metric_name: str
    start_time: datetime
    end_time: datetime
    dimensions: dict[str, str] = field(default_factory=dict)
    statistic: str = "Average"
    period: int = 60

    def as_cloudwatch_kwargs(self) -> dict[str, Any]:
        kwargs: dict[str, Any] = {
            "Namespace": self.metric_name.split("/")[0] if "/" in self.metric_name else "Custom/Observability",
            "MetricName": self.metric_name.split("/")[-1],
            "StartTime": self.start_time,
            "EndTime": self.end_time,
            "Period": self.period,
            "Statistics": [self.statistic],
        }
        if self.dimensions:
            kwargs["Dimensions"] = [{"Name": k, "Value": v} for k, v in self.dimensions.items()]
        return kwargs


@dataclass(slots=True)
class MetricSeriesPoint:
    timestamp: datetime
    value: float
    unit: str | None = None
    dimensions: dict[str, str] = field(default_factory=dict)


@dataclass(slots=True)
class MetricSeriesResult:
    metric_name: str
    points: list[MetricSeriesPoint] = field(default_factory=list)
    source: str = "amazon-cloudwatch"


@dataclass(slots=True)
class MetricStatsResult:
    metric_name: str
    minimum: float | None = None
    maximum: float | None = None
    average: float | None = None
    sum: float | None = None
    sample_count: float | None = None
    source: str = "amazon-cloudwatch"


@dataclass(slots=True)
class MetricComparisonResult:
    metric_name: str
    left_label: str
    right_label: str
    left_average: float | None = None
    right_average: float | None = None
    delta: float | None = None
    ratio: float | None = None
    source: str = "amazon-cloudwatch"


@dataclass(slots=True)
class MetricSummaryResult:
    metric_name: str
    trend: str
    anomaly_score: float | None = None
    latest_value: float | None = None
    baseline_value: float | None = None
    source: str = "amazon-cloudwatch"


@dataclass(slots=True)
class SafetyCheckResult:
    text: str
    safe: bool
    score: float | None = None
    categories: dict[str, float] = field(default_factory=dict)
    source: str = "perspective-api"


@dataclass(slots=True)
class TranslationResult:
    source_text: str
    translated_text: str
    target_language: str
    source_language: str | None = None
    provider: str = "deepL"


@dataclass(slots=True)
class ArchiveResult:
    bucket: str
    object_key: str
    etag: str | None = None
    url: str | None = None
    storage_provider: str = "amazon-s3"


def normalize_dimensions(dimensions: Optional[Mapping[str, str]] = None) -> dict[str, str]:
    return dict(dimensions or {})


def infer_time_window(minutes: int = 60) -> tuple[datetime, datetime]:
    end = utc_now()
    return end - timedelta(minutes=minutes), end
