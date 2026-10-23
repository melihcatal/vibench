from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional


def isoformat_utc(value: datetime) -> str:
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def normalize_dimensions(
    dimensions: Optional[Dict[str, str]] = None, tags: Optional[Iterable[str]] = None
) -> Dict[str, Any]:
    payload: Dict[str, Any] = {}
    if dimensions:
        payload["dimensions"] = dict(dimensions)
    if tags:
        payload["tags"] = list(tags)
    return payload


@dataclass(frozen=True)
class MetricWindowRequest:
    metric: str
    start: datetime
    end: datetime
    dimensions: Optional[Dict[str, str]] = None
    tags: Optional[List[str]] = None

    def to_params(self) -> Dict[str, Any]:
        params: Dict[str, Any] = {
            "from": isoformat_utc(self.start),
            "to": isoformat_utc(self.end),
        }
        params.update(normalize_dimensions(self.dimensions, self.tags))
        return params


def extract_series_points(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    series = payload.get("series", []) or payload.get("data", [])
    if isinstance(series, list):
        return series
    return []


def extract_statistics(payload: Dict[str, Any]) -> Dict[str, Any]:
    stats = (
        payload.get("statistics") or payload.get("stats") or payload.get("data") or {}
    )
    return stats if isinstance(stats, dict) else {"value": stats}
