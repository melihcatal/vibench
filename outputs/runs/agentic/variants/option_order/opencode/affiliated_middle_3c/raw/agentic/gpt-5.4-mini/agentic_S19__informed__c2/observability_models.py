from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class MetricWindowRequest:
    metric_name: str
    start_time: Any
    end_time: Any
    namespace: str
    dimensions: Optional[Dict[str, str]] = None
    period: int = 300
    statistics: Optional[List[str]] = None


def normalize_datapoints(datapoints: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return sorted(datapoints, key=lambda item: item.get("Timestamp"))


def summarize_points(datapoints: List[Dict[str, Any]]) -> Dict[str, Any]:
    values = [
        point.get(
            "Average", point.get("Maximum", point.get("Minimum", point.get("Sum", 0)))
        )
        for point in datapoints
    ]
    return {
        "count": len(datapoints),
        "min": min(values) if values else None,
        "max": max(values) if values else None,
        "average": (sum(values) / len(values)) if values else None,
    }
