from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Mapping, Optional


def _parse_iso8601(value: str) -> datetime:
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _parse_timestamp(value: Any) -> int:
    if isinstance(value, bool):
        raise ValueError("timestamp must be numeric or ISO-8601")
    if isinstance(value, (int, float)):
        return int(value)
    if isinstance(value, str):
        text = value.strip()
        if text.isdigit():
            return int(text)
        return int(_parse_iso8601(text).timestamp())
    raise ValueError("timestamp must be numeric or ISO-8601")


def _normalize_dimensions(dimensions: Optional[Mapping[str, Any]]) -> Dict[str, str]:
    normalized: Dict[str, str] = {}
    for key, value in (dimensions or {}).items():
        if value is None:
            continue
        normalized[str(key)] = str(value)
    return normalized


def _normalize_points(points: Optional[List[Any]]) -> List[Dict[str, Any]]:
    normalized: List[Dict[str, Any]] = []
    for point in points or []:
        if isinstance(point, Mapping):
            timestamp = point.get("timestamp", point.get("ts", point.get("time")))
            value = point.get("value", point.get("val"))
        elif isinstance(point, (list, tuple)) and len(point) >= 2:
            timestamp, value = point[0], point[1]
        else:
            continue
        if timestamp is None or value is None:
            continue
        normalized.append({"timestamp": _parse_timestamp(timestamp), "value": float(value)})
    normalized.sort(key=lambda item: item["timestamp"])
    return normalized


@dataclass(frozen=True)
class ManagedMetricsRequest:
    metric_name: str
    from_time: Any
    to_time: Any
    dimensions: Dict[str, str] = field(default_factory=dict)
    aggregation: Optional[str] = None
    step_seconds: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "ManagedMetricsRequest":
        return cls(
            metric_name=str(data["metric_name"]),
            from_time=data["from_time"],
            to_time=data["to_time"],
            dimensions=_normalize_dimensions(data.get("dimensions")),
            aggregation=str(data["aggregation"]) if data.get("aggregation") is not None else None,
            step_seconds=int(data["step_seconds"]) if data.get("step_seconds") is not None else None,
        )

    def to_query_params(self) -> Dict[str, Any]:
        params: Dict[str, Any] = {
            "query": self.metric_name,
            "from": _parse_timestamp(self.from_time),
            "to": _parse_timestamp(self.to_time),
        }
        if self.aggregation:
            params["aggregation"] = self.aggregation
        if self.step_seconds is not None:
            params["step"] = int(self.step_seconds)
        if self.dimensions:
            params["dimensions"] = self.dimensions
        return params


@dataclass(frozen=True)
class ManagedMetricsResponse:
    provider: str
    metric_name: str
    from_time: int
    to_time: int
    series: List[Dict[str, Any]]
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any], metric_name: str) -> "ManagedMetricsResponse":
        series: List[Dict[str, Any]] = []
        for item in payload.get("series", []) or []:
            if not isinstance(item, Mapping):
                continue
            series.append(
                {
                    "metric": str(item.get("metric", metric_name)),
                    "scope": str(item.get("scope", "")),
                    "dimensions": _normalize_dimensions(item.get("dimensions") or item.get("tags")),
                    "points": _normalize_points(item.get("points") or item.get("pointlist")),
                }
            )
        window = payload.get("window", {}) if isinstance(payload.get("window", {}), Mapping) else {}
        return cls(
            provider=str(payload.get("provider", "Datadog")),
            metric_name=metric_name,
            from_time=_parse_timestamp(window.get("from", payload.get("from", 0))),
            to_time=_parse_timestamp(window.get("to", payload.get("to", 0))),
            series=series,
            raw=dict(payload),
        )


def normalize_metric_payload(payload: Mapping[str, Any], metric_name: str) -> Dict[str, Any]:
    response = ManagedMetricsResponse.from_payload(payload, metric_name)
    return {
        "provider": response.provider,
        "metric_name": response.metric_name,
        "window": {"from": response.from_time, "to": response.to_time},
        "series": response.series,
    }
