from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional


@dataclass(slots=True)
class MetricWindowRequest:
    metric_name: str
    start_time: datetime
    end_time: datetime
    dimensions: Dict[str, str] = field(default_factory=dict)
    resource: Optional[str] = None
    aggregation: str = "average"
    limit: int = 100

    def normalized(self) -> "MetricWindowRequest":
        return MetricWindowRequest(
            metric_name=self.metric_name.strip(),
            start_time=self._ensure_utc(self.start_time),
            end_time=self._ensure_utc(self.end_time),
            dimensions=dict(sorted((k.strip(), v.strip()) for k, v in self.dimensions.items())),
            resource=self.resource.strip() if self.resource else None,
            aggregation=self.aggregation.strip().lower(),
            limit=max(1, int(self.limit)),
        )

    @staticmethod
    def _ensure_utc(value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)


@dataclass(slots=True)
class MetricDatapoint:
    timestamp: datetime
    value: float
    dimensions: Dict[str, str] = field(default_factory=dict)


@dataclass(slots=True)
class MetricSeriesResponse:
    metric_name: str
    datapoints: List[MetricDatapoint]
    raw: Any = None


@dataclass(slots=True)
class MetricStatsResponse:
    metric_name: str
    minimum: Optional[float] = None
    maximum: Optional[float] = None
    average: Optional[float] = None
    total: Optional[float] = None
    count: Optional[int] = None
    raw: Any = None


@dataclass(slots=True)
class MetricComparisonResponse:
    metric_name: str
    left_label: str
    right_label: str
    left_series: List[MetricDatapoint]
    right_series: List[MetricDatapoint]
    raw: Any = None


@dataclass(slots=True)
class MetricSummary:
    metric_name: str
    trend: str
    anomaly_score: float
    summary: str
    raw: Any = None


@dataclass(slots=True)
class AnnotationSafetyResult:
    text: str
    safe: bool
    risk_score: float
    provider_result: Any = None


@dataclass(slots=True)
class TranslationResult:
    source_text: str
    translated_text: str
    source_locale: str
    target_locale: str
    provider_result: Any = None


@dataclass(slots=True)
class ArchiveResult:
    bucket: str
    key: str
    etag: Optional[str] = None
    uri: Optional[str] = None
    raw: Any = None


def parse_iso8601(value: str) -> datetime:
    text = value.strip().replace("Z", "+00:00")
    return datetime.fromisoformat(text)


def serialize_datapoints(items: Iterable[Mapping[str, Any]]) -> List[MetricDatapoint]:
    result: List[MetricDatapoint] = []
    for item in items:
        ts = item.get("timestamp") or item.get("time") or item.get("datetime")
        if isinstance(ts, str):
            ts_dt = parse_iso8601(ts)
        elif isinstance(ts, datetime):
            ts_dt = ts
        else:
            ts_dt = datetime.now(timezone.utc)
        value = item.get("value")
        if value is None:
            value = item.get("sum") or item.get("avg") or item.get("average") or 0.0
        dimensions = dict(item.get("dimensions") or item.get("tags") or {})
        result.append(MetricDatapoint(timestamp=ts_dt, value=float(value), dimensions=dimensions))
    return result


def flatten_dimensions(dimensions: Mapping[str, str]) -> str:
    return ",".join(f"{k}:{v}" for k, v in sorted(dimensions.items()))


def normalize_text(text: str) -> str:
    return " ".join(text.split()).strip()
