from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class MetricWindowRequest:
    metric_name: str
    start_time: datetime
    end_time: datetime
    period: int = 300
    namespace: str = "ManagedMetrics"


@dataclass(frozen=True)
class MetricQueryResponse:
    label: str
    timestamps: list
    values: list
    status_code: str


def normalize_datapoints(datapoints):
    ordered = sorted(datapoints, key=lambda item: item.get("Timestamp"))
    return [
        {
            "timestamp": item.get("Timestamp"),
            "value": item.get(
                "Average", item.get("Sum", item.get("Maximum", item.get("Minimum")))
            ),
        }
        for item in ordered
    ]
