from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional


@dataclass
class MetricWindowRequest:
    metric_name: str
    start_time: str
    end_time: str
    resource_id: Optional[str] = None
    dimensions: Optional[Dict[str, str]] = None


@dataclass
class MetricSeriesPoint:
    timestamp: str
    value: float


@dataclass
class MetricResponse:
    metric_name: str
    points: List[MetricSeriesPoint]
    summary: Dict[str, Any]


def normalize_request(request: MetricWindowRequest) -> Dict[str, Any]:
    payload = asdict(request)
    return {k: v for k, v in payload.items() if v is not None}
