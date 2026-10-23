from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Mapping, Optional

from observability_client import ObservabilityClient, create_client
from observability_models import MetricSummary, normalize_metric_summary


@dataclass(frozen=True)
class MetricSummaryRequest:
    metric_name: str
    start_time: datetime
    end_time: datetime
    resource: Optional[str] = None
    dimensions: Mapping[str, Any] = None

    def to_query_params(self) -> Dict[str, Any]:
        params: Dict[str, Any] = {
            "metric_name": self.metric_name,
            "start_time": _ensure_utc(self.start_time),
            "end_time": _ensure_utc(self.end_time),
        }
        if self.resource:
            params["resource"] = self.resource
        if self.dimensions:
            for key, value in self.dimensions.items():
                params[f"dimension.{key}"] = value
        return params


def _ensure_utc(value: datetime) -> datetime:
    return value if value.tzinfo else value.replace(tzinfo=timezone.utc)


def summarize_metric_trends(
    metric_name: str,
    start_time: datetime,
    end_time: datetime,
    resource: Optional[str] = None,
    dimensions: Optional[Mapping[str, Any]] = None,
    client: Optional[ObservabilityClient] = None,
) -> MetricSummary:
    active_client = client or create_client()
    request = MetricSummaryRequest(
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        resource=resource,
        dimensions=dimensions or {},
    )
    payload = active_client.get_json("/api/v1/metrics/summary", params=request.to_query_params())
    return normalize_metric_summary(payload)


def summarize_recent_metric(
    metric_name: str,
    minutes: int = 60,
    resource: Optional[str] = None,
    dimensions: Optional[Mapping[str, Any]] = None,
    client: Optional[ObservabilityClient] = None,
) -> MetricSummary:
    end_time = datetime.now(timezone.utc)
    start_time = end_time - __import__("datetime").timedelta(minutes=minutes)
    return summarize_metric_trends(
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        resource=resource,
        dimensions=dimensions,
        client=client,
    )
