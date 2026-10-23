from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class MetricWindowRequest:
    metric_name: str
    start_time: datetime
    end_time: datetime
    filters: Optional[Dict[str, str]] = None


@dataclass
class MetricSeriesPoint:
    timestamp: datetime
    value: float
    dimensions: Dict[str, str]


@dataclass
class MetricSeriesResponse:
    metric_name: str
    points: List[MetricSeriesPoint]


def normalize_dimensions(dimensions: Optional[Dict[str, Any]]) -> Dict[str, str]:
    if not dimensions:
        return {}
    return {str(k): str(v) for k, v in dimensions.items() if v is not None}


def parse_iso_datetime(value: Any) -> datetime:
    if isinstance(value, datetime):
        return value
    text = str(value).replace("Z", "+00:00")
    return datetime.fromisoformat(text)
