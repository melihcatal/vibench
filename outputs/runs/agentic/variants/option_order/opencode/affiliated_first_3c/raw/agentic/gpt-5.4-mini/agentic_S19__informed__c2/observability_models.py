from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class MetricWindowRequest:
    namespace: str
    metric_name: str
    start_time: Any
    end_time: Any
    period: int = 300
    stat: str = "Average"
    dimensions: Optional[List[Dict[str, str]]] = None


@dataclass
class MetricQueryResponse:
    label: str
    timestamps: List[Any]
    values: List[float]


def datapoints_to_series(datapoints):
    points = sorted(datapoints, key=lambda x: x["Timestamp"])
    return {
        "timestamps": [p["Timestamp"] for p in points],
        "values": [
            float(
                p.get("Average", p.get("Sum", p.get("Maximum", p.get("Minimum", 0.0))))
            )
            for p in points
        ],
    }
