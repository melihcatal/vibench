from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class MetricWindowRequest:
    metric: str
    start: datetime
    end: datetime
    tags: Optional[List[str]] = None
    group_by: Optional[List[str]] = None
    aggregator: str = "avg"


@dataclass
class MetricSeries:
    metric: str
    points: List[List[float]]
    scope: str = ""
    tags: Optional[List[str]] = None


@dataclass
class MetricStats:
    metric: str
    start: datetime
    end: datetime
    avg: Optional[float] = None
    min: Optional[float] = None
    max: Optional[float] = None
    sum: Optional[float] = None
    count: Optional[float] = None


@dataclass
class MetricComparison:
    left: MetricSeries
    right: MetricSeries
    delta: List[float]



def isoformat_utc(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def normalize_tags(tags: Optional[Iterable[str]]) -> List[str]:
    return [tag.strip() for tag in tags or [] if tag and tag.strip()]


def parse_datadog_series(payload: Dict[str, Any]) -> List[MetricSeries]:
    results: List[MetricSeries] = []
    for item in payload.get("series", []):
        results.append(
            MetricSeries(
                metric=item.get("metric", ""),
                points=item.get("pointlist", []),
                scope=item.get("scope", ""),
                tags=item.get("tag_set") or None,
            )
        )
    return results
