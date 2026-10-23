from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional


def normalize_dimensions(dimensions: Optional[Dict[str, str]] = None) -> List[Dict[str, str]]:
    return [{"Name": k, "Value": v} for k, v in (dimensions or {}).items()]


def normalize_datapoints(datapoints: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return sorted(
        [{k: v for k, v in point.items()} for point in datapoints],
        key=lambda p: p.get("Timestamp", datetime.min),
    )


@dataclass
class MetricWindowRequest:
    namespace: str
    metric_name: str
    start_time: datetime
    end_time: datetime
    dimensions: Dict[str, str] = field(default_factory=dict)
    period: int = 300
    statistics: List[str] = field(default_factory=lambda: ["Average"])


@dataclass
class MetricSeriesResponse:
    metric_name: str
    namespace: str
    datapoints: List[Dict[str, Any]]
