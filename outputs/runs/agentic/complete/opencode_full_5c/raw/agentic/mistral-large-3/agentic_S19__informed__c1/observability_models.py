from typing import Dict, List, Optional, Union
from datetime import datetime
from dataclasses import dataclass


@dataclass
class MetricPoint:
    timestamp: str
    value: Union[float, int]
    resource_labels: Dict[str, str]
    metric_labels: Dict[str, str]


@dataclass
class MetricStats:
    count: int
    mean: float
    min: float
    max: float
    sum: float
    series: List[Dict]


@dataclass
class MetricComparison:
    series_a: List[Dict]
    series_b: List[Dict]
    comparison_stats: Dict[str, Union[int, float, None]]


@dataclass
class MetricDescriptor:
    type: str
    name: str
    description: str
    labels: List[Dict[str, str]]
    metric_kind: str
    value_type: str


def normalize_metric_descriptor(descriptor) -> MetricDescriptor:
    return MetricDescriptor(
        type=descriptor.type,
        name=descriptor.name,
        description=descriptor.description,
        labels=[
            {"key": label.key, "description": label.description}
            for label in descriptor.labels
        ],
        metric_kind=descriptor.metric_kind.name,
        value_type=descriptor.value_type.name,
    )


def parse_metric_points(time_series_data: List[Dict]) -> List[MetricPoint]:
    return [
        MetricPoint(
            timestamp=data.get("timestamp"),
            value=data.get("value"),
            resource_labels=data.get("resource_labels", {}),
            metric_labels=data.get("metric_labels", {}),
        )
        for data in time_series_data
    ]
