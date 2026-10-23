from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union


def _parse_iso8601(value: Union[str, datetime]) -> datetime:
    if isinstance(value, datetime):
        dt = value
    else:
        normalized = value.replace("Z", "+00:00")
        dt = datetime.fromisoformat(normalized)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _dt_to_iso8601(value: datetime) -> str:
    return _parse_iso8601(value).isoformat()


def _coerce_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _coerce_int(value: Any) -> Optional[int]:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _coerce_str_list(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, Sequence):
        return [str(item) for item in value if item is not None]
    return [str(value)]


@dataclass(frozen=True)
class MetricWindowRequest:
    metric_name: str
    start_time: datetime
    end_time: datetime
    project_id: Optional[str] = None
    resource_labels: Mapping[str, str] = field(default_factory=dict)
    dimensions: Mapping[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "metric_name": self.metric_name,
            "start_time": _dt_to_iso8601(self.start_time),
            "end_time": _dt_to_iso8601(self.end_time),
            "project_id": self.project_id,
            "resource_labels": dict(self.resource_labels),
            "dimensions": dict(self.dimensions),
        }


@dataclass(frozen=True)
class MetricSeriesComparisonRequest:
    metric_name: str
    left_filter: Mapping[str, str]
    right_filter: Mapping[str, str]
    start_time: datetime
    end_time: datetime
    project_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "metric_name": self.metric_name,
            "left_filter": dict(self.left_filter),
            "right_filter": dict(self.right_filter),
            "start_time": _dt_to_iso8601(self.start_time),
            "end_time": _dt_to_iso8601(self.end_time),
            "project_id": self.project_id,
        }


@dataclass(frozen=True)
class MetricStatSummary:
    count: int
    minimum: Optional[float]
    maximum: Optional[float]
    average: Optional[float]
    sum: float

    @classmethod
    def from_values(cls, values: Sequence[Any]) -> "MetricStatSummary":
        numeric = [float(v) for v in values if _coerce_float(v) is not None]
        count = len(numeric)
        total = float(sum(numeric)) if numeric else 0.0
        return cls(
            count=count,
            minimum=min(numeric) if numeric else None,
            maximum=max(numeric) if numeric else None,
            average=(total / count) if count else None,
            sum=total,
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class MetricDatapoint:
    timestamp: datetime
    value: float
    dimensions: Mapping[str, str] = field(default_factory=dict)

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> Optional["MetricDatapoint"]:
        ts = payload.get("timestamp") or payload.get("time") or payload.get("date")
        val = payload.get("value") or payload.get("count") or payload.get("total")
        if ts is None or val is None:
            return None
        return cls(
            timestamp=_parse_iso8601(str(ts)),
            value=float(val),
            dimensions={str(k): str(v) for k, v in dict(payload.get("dimensions", {})).items()},
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": _dt_to_iso8601(self.timestamp),
            "value": self.value,
            "dimensions": dict(self.dimensions),
        }


@dataclass(frozen=True)
class MetricSeries:
    metric_name: str
    points: List[MetricDatapoint]
    labels: Mapping[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "metric_name": self.metric_name,
            "points": [point.to_dict() for point in self.points],
            "labels": dict(self.labels),
        }


@dataclass(frozen=True)
class MetricWindowResponse:
    metric_name: str
    start_time: datetime
    end_time: datetime
    points: List[MetricDatapoint]
    summary: MetricStatSummary
    project_id: Optional[str] = None

    @classmethod
    def from_payload(cls, metric_name: str, payload: Mapping[str, Any], start_time: Union[str, datetime], end_time: Union[str, datetime], project_id: Optional[str] = None) -> "MetricWindowResponse":
        points_payload = payload.get("data", []) if isinstance(payload, Mapping) else []
        points = []
        for item in points_payload:
            if isinstance(item, Mapping):
                point = MetricDatapoint.from_payload(item)
                if point is not None:
                    points.append(point)
        return cls(
            metric_name=metric_name,
            start_time=_parse_iso8601(start_time),
            end_time=_parse_iso8601(end_time),
            points=points,
            summary=MetricStatSummary.from_values([p.value for p in points]),
            project_id=project_id,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "metric_name": self.metric_name,
            "start_time": _dt_to_iso8601(self.start_time),
            "end_time": _dt_to_iso8601(self.end_time),
            "points": [point.to_dict() for point in self.points],
            "summary": self.summary.to_dict(),
            "project_id": self.project_id,
        }


@dataclass(frozen=True)
class MetricComparisonResponse:
    metric_name: str
    left_summary: MetricStatSummary
    right_summary: MetricStatSummary
    start_time: datetime
    end_time: datetime
    project_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "metric_name": self.metric_name,
            "left_summary": self.left_summary.to_dict(),
            "right_summary": self.right_summary.to_dict(),
            "start_time": _dt_to_iso8601(self.start_time),
            "end_time": _dt_to_iso8601(self.end_time),
            "project_id": self.project_id,
        }


@dataclass(frozen=True)
class MetricAnnotationSafetyRequest:
    text: str
    locale: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {"text": self.text, "locale": self.locale}


@dataclass(frozen=True)
class MetricAnnotationSafetyResult:
    safe: bool
    reasons: List[str]
    normalized_text: str

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> "MetricAnnotationSafetyResult":
        return cls(
            safe=bool(payload.get("safe", False)),
            reasons=_coerce_str_list(payload.get("reasons", [])),
            normalized_text=str(payload.get("normalized_text", "")),
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DashboardNoteTranslationRequest:
    text: str
    target_locale: str
    source_locale: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "target_locale": self.target_locale,
            "source_locale": self.source_locale,
        }


@dataclass(frozen=True)
class DashboardNoteTranslationResult:
    translated_text: str
    target_locale: str
    source_locale: Optional[str] = None

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> "DashboardNoteTranslationResult":
        return cls(
            translated_text=str(payload.get("translated_text", payload.get("text", ""))),
            target_locale=str(payload.get("target_locale", "")),
            source_locale=payload.get("source_locale"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def normalize_metric_payload(payload: Mapping[str, Any]) -> Dict[str, Any]:
    normalized: Dict[str, Any] = dict(payload)
    if "timestamp" in normalized:
        normalized["timestamp"] = _dt_to_iso8601(_parse_iso8601(str(normalized["timestamp"])))
    if "start_time" in normalized:
        normalized["start_time"] = _dt_to_iso8601(_parse_iso8601(str(normalized["start_time"])))
    if "end_time" in normalized:
        normalized["end_time"] = _dt_to_iso8601(_parse_iso8601(str(normalized["end_time"])))
    for key in ("value", "count", "total", "average", "min", "max", "sum"):
        if key in normalized:
            coerced = _coerce_float(normalized[key])
            if coerced is not None:
                normalized[key] = coerced
    for key in ("points", "datapoints", "data"):
        if key in normalized and isinstance(normalized[key], list):
            normalized[key] = [normalize_metric_payload(item) if isinstance(item, Mapping) else item for item in normalized[key]]
    return normalized


def summarize_metric_values(values: Sequence[Any]) -> MetricStatSummary:
    return MetricStatSummary.from_values(values)
