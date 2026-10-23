from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple


def _coerce_timestamp(value: Any) -> int:
    if isinstance(value, bool):
        raise TypeError("timestamp must be an int or datetime-like value")
    if isinstance(value, (int, float)):
        return int(value)
    if isinstance(value, str):
        if value.isdigit():
            return int(value)
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return int(dt.timestamp())
    if isinstance(value, datetime):
        dt = value if value.tzinfo is not None else value.replace(tzinfo=timezone.utc)
        return int(dt.timestamp())
    raise TypeError("unsupported timestamp value")


def _coerce_float(value: Any) -> float:
    if value is None:
        raise TypeError("value cannot be None")
    return float(value)


def _normalize_points(points: Any) -> List[Tuple[int, float]]:
    normalized: List[Tuple[int, float]] = []
    if not points:
        return normalized
    for item in points:
        if isinstance(item, Mapping):
            ts = item.get("timestamp", item.get("ts", item.get("time")))
            val = item.get("value", item.get("v", item.get("point")))
            if isinstance(val, Sequence) and len(val) == 2 and not isinstance(val, (str, bytes)):
                ts, val = val
        else:
            ts, val = item
        if val is None:
            continue
        normalized.append((_coerce_timestamp(ts), _coerce_float(val)))
    return normalized


def _summary(points: Sequence[Tuple[int, float]]) -> Dict[str, Optional[float]]:
    values = [value for _, value in points]
    if not values:
        return {"count": 0, "min": None, "max": None, "avg": None, "last": None}
    return {
        "count": len(values),
        "min": min(values),
        "max": max(values),
        "avg": sum(values) / len(values),
        "last": values[-1],
    }


@dataclass(frozen=True)
class ManagedMetricsMonitoringRequest:
    provider: str
    metric: str
    start: int
    end: int
    filters: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> "ManagedMetricsMonitoringRequest":
        return cls(
            provider=str(payload.get("provider", "datadog")),
            metric=str(payload["metric"]),
            start=_coerce_timestamp(payload["start"]),
            end=_coerce_timestamp(payload["end"]),
            filters=dict(payload.get("filters", {})),
        )

    def to_query_params(self) -> Dict[str, Any]:
        params: Dict[str, Any] = {"query": self.metric, "from": self.start, "to": self.end}
        params.update(self.filters)
        return params


@dataclass(frozen=True)
class ManagedMetricsMonitoringResponse:
    provider: str
    metric: str
    window: Dict[str, int]
    points: List[Tuple[int, float]]
    summary: Dict[str, Optional[float]]
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any], provider: str = "datadog") -> "ManagedMetricsMonitoringResponse":
        metric = str(payload.get("metric", payload.get("query", "")))
        window = payload.get("window", {})
        points = _normalize_points(payload.get("points", payload.get("series", [])))
        if not window and payload.get("from") is not None and payload.get("to") is not None:
            window = {"start": _coerce_timestamp(payload["from"]), "end": _coerce_timestamp(payload["to"])}
        normalized_window = {
            "start": _coerce_timestamp(window.get("start", payload.get("from"))),
            "end": _coerce_timestamp(window.get("end", payload.get("to"))),
        }
        return cls(
            provider=provider,
            metric=metric,
            window=normalized_window,
            points=points,
            summary=_summary(points),
            raw=dict(payload),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "metric": self.metric,
            "window": dict(self.window),
            "points": list(self.points),
            "summary": dict(self.summary),
            "raw": dict(self.raw),
        }


def normalize_managed_metrics_payload(payload: Mapping[str, Any], provider: str = "datadog") -> ManagedMetricsMonitoringResponse:
    return ManagedMetricsMonitoringResponse.from_payload(payload, provider=provider)
