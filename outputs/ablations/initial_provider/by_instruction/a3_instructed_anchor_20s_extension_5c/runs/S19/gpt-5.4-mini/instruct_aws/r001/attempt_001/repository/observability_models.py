from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Mapping, Optional


def normalize_dimensions(dimensions: Optional[Mapping[str, str]]) -> List[Dict[str, str]]:
    if not dimensions:
        return []
    return [{"Name": str(k), "Value": str(v)} for k, v in sorted(dimensions.items())]


@dataclass
class MetricWindowRequest:
    namespace: str
    metric_name: str
    start_time: datetime
    end_time: datetime
    period: int = 300
    statistics: List[str] = field(default_factory=lambda: ["Average"])
    dimensions: Optional[Mapping[str, str]] = None


@dataclass
class MetricWindowResponse:
    timestamps: List[datetime]
    values: List[float]
    metadata: Dict[str, Any]
