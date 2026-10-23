from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional


def normalize_time(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.isoformat() + "Z" if value.tzinfo is None else value.isoformat()
    return str(value)


@dataclass
class MetricWindowRequest:
    metric_type: str
    start_time: str
    end_time: str
    alignment_period: Optional[str] = None
    filter_expression: Optional[str] = None


@dataclass
class MetricPointSeries:
    time_series: List[Dict[str, Any]]
