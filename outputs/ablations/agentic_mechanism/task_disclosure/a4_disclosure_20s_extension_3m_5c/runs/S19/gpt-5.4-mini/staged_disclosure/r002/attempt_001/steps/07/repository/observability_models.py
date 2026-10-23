from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple


def _normalize_timestamp(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(float(value), tz=timezone.utc).isoformat().replace("+00:00", "Z")
    if isinstance(value, datetime):
        dt = value if value.tzinfo else value.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    text = str(value).strip()
    if not text:
        return None
    if text.isdigit():
        return datetime.fromtimestamp(int(text), tz=timezone.utc).isoformat().replace("+00:00", "Z")
    parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _coerce_float(value: Any) -> Optional[float]:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _coerce_int(value: Any) -> Optional[int]:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


@dataclass(frozen=True)
class ManagedMetricsRequest:
    metric: str
    start: Optional[str] = None
    end: Optional[str] = None
    step: Optional[str] = None
    filters: Tuple[str, ...] = ()
    aggregation: Optional[str] = None
    dimensions: Tuple[str, ...] = ()

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "ManagedMetricsRequest":
        return cls(
            metric=str(data["metric"]),
            start=_normalize_timestamp(data.get("start")),
            end=_normalize_timestamp(data.get("end")),
            step=str(data["step"]) if data.get("step") is not None else None,
            filters=tuple(str(item) for item in data.get("filters", []) or ()),
            aggregation=str(data["aggregation"]) if data.get("aggregation") is not None else None,
            dimensions=tuple(str(item) for item in data.get("dimensions", []) or ()),
        )

    def to_query_params(self) -> Dict[str, Any]:
        params: Dict[str, Any] = {"metric": self.metric}
        if self.start:
            params["start"] = self.start
        if self.end:
            params["end"] = self.end
        if self.step:
            params["step"] = self.step
        if self.filters:
            params["filter"] = list(self.filters)
        if self.aggregation:
            params["aggregation"] = self.aggregation
        if self.dimensions:
            params["dimensions"] = list(self.dimensions)
        return params


@dataclass(frozen=True)
class ManagedMetricsPoint:
    timestamp: Optional[str]
    value: Optional[float]

    @classmethod
    def from_any(cls, data: Any) -> "ManagedMetricsPoint":
        if isinstance(data, Mapping):
            return cls(timestamp=_normalize_timestamp(data.get("timestamp") or data.get("ts") or data.get("time")), value=_coerce_float(data.get("value")))
        if isinstance(data, Sequence) and not isinstance(data, (str, bytes)) and len(data) >= 2:
            return cls(timestamp=_normalize_timestamp(data[0]), value=_coerce_float(data[1]))
        return cls(timestamp=None, value=_coerce_float(data))


@dataclass(frozen=True)
class ManagedMetricsResponse:
    metric: str
    start: Optional[str] = None
    end: Optional[str] = None
    count: int = 0
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    avg_value: Optional[float] = None
    sum_value: float = 0.0
    datapoints: Tuple[ManagedMetricsPoint, ...] = ()
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "ManagedMetricsResponse":
        points: List[ManagedMetricsPoint] = []
        for item in data.get("datapoints", []) or data.get("points", []) or data.get("series", []) or []:
            if isinstance(item, Mapping) and "pointlist" in item:
                for pt in item.get("pointlist", []) or []:
                    points.append(ManagedMetricsPoint.from_any(pt))
            else:
                points.append(ManagedMetricsPoint.from_any(item))

        values = [p.value for p in points if p.value is not None]
        count = _coerce_int(data.get("count")) or len(values)
        total = float(data.get("sum", sum(values) if values else 0.0))
        avg = _coerce_float(data.get("avg"))
        if avg is None and values:
            avg = total / len(values)
        return cls(
            metric=str(data.get("metric", "")),
            start=_normalize_timestamp(data.get("start")),
            end=_normalize_timestamp(data.get("end")),
            count=count,
            min_value=_coerce_float(data.get("min")) if data.get("min") is not None else (min(values) if values else None),
            max_value=_coerce_float(data.get("max")) if data.get("max") is not None else (max(values) if values else None),
            avg_value=avg,
            sum_value=total,
            datapoints=tuple(points),
            raw=dict(data),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "metric": self.metric,
            "start": self.start,
            "end": self.end,
            "count": self.count,
            "min": self.min_value,
            "max": self.max_value,
            "avg": self.avg_value,
            "sum": self.sum_value,
            "datapoints": [
                {"timestamp": point.timestamp, "value": point.value} for point in self.datapoints
            ],
        }


def normalize_managed_metrics_request(data: Mapping[str, Any]) -> Dict[str, Any]:
    return ManagedMetricsRequest.from_mapping(data).to_query_params()


def normalize_managed_metrics_response(data: Mapping[str, Any]) -> Dict[str, Any]:
    return ManagedMetricsResponse.from_mapping(data).to_dict()
