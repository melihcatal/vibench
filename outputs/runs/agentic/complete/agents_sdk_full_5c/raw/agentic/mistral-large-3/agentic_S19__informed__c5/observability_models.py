from typing import List, Dict, Any, Optional
from datetime import datetime


class MetricPoint:
    def __init__(
        self,
        interval_start: datetime,
        interval_end: datetime,
        value: float,
    ):
        self.interval_start = interval_start
        self.interval_end = interval_end
        self.value = value

    def to_dict(self) -> Dict[str, Any]:
        return {
            "interval": {
                "start_time": self.interval_start.isoformat(),
                "end_time": self.interval_end.isoformat(),
            },
            "value": self.value,
        }


class MetricSeries:
    def __init__(
        self,
        metric_type: str,
        metric_labels: Dict[str, str],
        resource_type: str,
        resource_labels: Dict[str, str],
        points: List[MetricPoint],
    ):
        self.metric_type = metric_type
        self.metric_labels = metric_labels
        self.resource_type = resource_type
        self.resource_labels = resource_labels
        self.points = points

    def to_dict(self) -> Dict[str, Any]:
        return {
            "metric": {
                "type": self.metric_type,
                "labels": self.metric_labels,
            },
            "resource": {
                "type": self.resource_type,
                "labels": self.resource_labels,
            },
            "points": [point.to_dict() for point in self.points],
        }


def normalize_metric_response(raw_response: List[Dict[str, Any]]) -> List[MetricSeries]:
    normalized = []
    for series in raw_response:
        points = [
            MetricPoint(
                interval_start=point["interval"]["start_time"],
                interval_end=point["interval"]["end_time"],
                value=point["value"],
            )
            for point in series["points"]
        ]
        normalized.append(
            MetricSeries(
                metric_type=series["metric"]["type"],
                metric_labels=series["metric"]["labels"],
                resource_type=series["resource"]["type"],
                resource_labels=series["resource"]["labels"],
                points=points,
            )
        )
    return normalized