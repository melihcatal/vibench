import os
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Iterable, List, Optional


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def coerce_window(start_time: Optional[datetime] = None, end_time: Optional[datetime] = None, lookback_minutes: int = 60):
    end = end_time or utc_now()
    start = start_time or (end - timedelta(minutes=lookback_minutes))
    if start.tzinfo is None:
        start = start.replace(tzinfo=timezone.utc)
    if end.tzinfo is None:
        end = end.replace(tzinfo=timezone.utc)
    return start, end


def isoformat(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat().replace('+00:00', 'Z')


def normalize_tags(tags: Optional[Dict[str, str]] = None, dimensions: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    merged = {}
    for source in (tags or {}, dimensions or {}):
        for k, v in source.items():
            if v is not None:
                merged[str(k)] = str(v)
    return merged


def normalize_points(points: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out = []
    for point in points or []:
        p = dict(point)
        if 'timestamp' in p and isinstance(p['timestamp'], str) and p['timestamp'].endswith('Z'):
            p['timestamp'] = p['timestamp']
        out.append(p)
    return out


@dataclass
class MetricQuery:
    metric: str
    start_time: datetime
    end_time: datetime
    filters: Dict[str, str] = field(default_factory=dict)
    aggregation: Optional[str] = None
    limit: int = 1000

    def to_params(self) -> Dict[str, Any]:
        params = {
            'from': isoformat(self.start_time),
            'to': isoformat(self.end_time),
            'query': self.metric,
            'page[size]': self.limit,
        }
        if self.aggregation:
            params['aggregation'] = self.aggregation
        for k, v in self.filters.items():
            params[f'tag_filters[{k}]'] = v
        return params


@dataclass
class MetricSeriesComparison:
    left: Dict[str, str]
    right: Dict[str, str]
    metric: str
    start_time: datetime
    end_time: datetime

