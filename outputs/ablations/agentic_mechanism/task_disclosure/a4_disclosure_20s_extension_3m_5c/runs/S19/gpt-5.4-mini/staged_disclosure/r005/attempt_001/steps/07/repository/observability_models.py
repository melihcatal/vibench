from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, Optional


def _utc_datetime(value: Any) -> datetime:
    if isinstance(value, datetime):
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value, tz=timezone.utc)
    if isinstance(value, str):
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)
    raise TypeError(f"Unsupported datetime value: {value!r}")


def _normalize_labels(labels: Optional[Mapping[str, Any]]) -> Dict[str, str]:
    if not labels:
        return {}
    return {str(key): str(value) for key, value in labels.items() if value is not None}


def _normalize_points(points: Optional[Iterable[Any]]) -> List[Dict[str, Any]]:
    normalized: List[Dict[str, Any]] = []
    if not points:
        return normalized
    for point in points:
        if isinstance(point, Mapping):
            timestamp = point.get("timestamp") or point.get("time") or point.get("end_time")
            normalized.append(
                {
                    "timestamp": _utc_datetime(timestamp).isoformat() if timestamp is not None else None,
                    "value": point.get("value"),
                    "labels": _normalize_labels(point.get("labels")),
                }
            )
        else:
            normalized.append({"timestamp": None, "value": point, "labels": {}})
    return normalized


@dataclass(frozen=True)
class ManagedMetricsRequest:
    metric_name: str
    resource_type: Optional[str] = None
    labels: Dict[str, str] = field(default_factory=dict)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    granularity_seconds: Optional[int] = None

    def normalized(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"metric_name": self.metric_name}
        if self.resource_type is not None:
            payload["resource_type"] = self.resource_type
        if self.labels:
            payload["labels"] = _normalize_labels(self.labels)
        if self.start_time is not None:
            payload["start_time"] = _utc_datetime(self.start_time).isoformat()
        if self.end_time is not None:
            payload["end_time"] = _utc_datetime(self.end_time).isoformat()
        if self.granularity_seconds is not None:
            payload["granularity_seconds"] = int(self.granularity_seconds)
        return payload


@dataclass(frozen=True)
class ManagedMetricsResponse:
    provider: str
    request: ManagedMetricsRequest
    points: List[Dict[str, Any]] = field(default_factory=list)
    summary: Dict[str, Any] = field(default_factory=dict)

    def normalized(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "request": self.request.normalized(),
            "points": _normalize_points(self.points),
            "summary": dict(self.summary),
        }


def normalize_managed_metrics_request(payload: Mapping[str, Any]) -> Dict[str, Any]:
    request = ManagedMetricsRequest(
        metric_name=str(payload.get("metric_name", "")),
        resource_type=payload.get("resource_type"),
        labels=_normalize_labels(payload.get("labels")),
        start_time=_utc_datetime(payload["start_time"]) if payload.get("start_time") is not None else None,
        end_time=_utc_datetime(payload["end_time"]) if payload.get("end_time") is not None else None,
        granularity_seconds=payload.get("granularity_seconds"),
    )
    return request.normalized()


def normalize_managed_metrics_response(payload: Mapping[str, Any]) -> Dict[str, Any]:
    request_payload = payload.get("request") or {}
    request = ManagedMetricsRequest(
        metric_name=str(request_payload.get("metric_name", payload.get("metric_name", ""))),
        resource_type=request_payload.get("resource_type", payload.get("resource_type")),
        labels=_normalize_labels(request_payload.get("labels", payload.get("labels"))),
        start_time=_utc_datetime(request_payload["start_time"]) if request_payload.get("start_time") is not None else None,
        end_time=_utc_datetime(request_payload["end_time"]) if request_payload.get("end_time") is not None else None,
        granularity_seconds=request_payload.get("granularity_seconds", payload.get("granularity_seconds")),
    )
    response = ManagedMetricsResponse(
        provider=str(payload.get("provider", "managed_metrics")),
        request=request,
        points=_normalize_points(payload.get("points")),
        summary=dict(payload.get("summary") or {}),
    )
    return response.normalized()
