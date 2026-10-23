from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional, Tuple


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def normalize_dimensions(
    dimensions: Optional[Dict[str, str]] = None,
) -> List[Dict[str, str]]:
    if not dimensions:
        return []
    return [{"Name": str(k), "Value": str(v)} for k, v in sorted(dimensions.items())]


def normalize_datapoints(datapoints: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    items = list(datapoints)
    return sorted(items, key=lambda p: p.get("Timestamp") or utc_now())


@dataclass(frozen=True)
class MetricWindowRequest:
    metric_name: str
    namespace: str
    start_time: datetime
    end_time: datetime
    period: int = 300
    statistics: Tuple[str, ...] = ("Average",)
    dimensions: Optional[Dict[str, str]] = None


@dataclass(frozen=True)
class MetricComparisonRequest:
    metric_name: str
    namespace: str
    start_time: datetime
    end_time: datetime
    period: int = 300
    statistics: Tuple[str, ...] = ("Average",)
    left_dimensions: Optional[Dict[str, str]] = None
    right_dimensions: Optional[Dict[str, str]] = None
