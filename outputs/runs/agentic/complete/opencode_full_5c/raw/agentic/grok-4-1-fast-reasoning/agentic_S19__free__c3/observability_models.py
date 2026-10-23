from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Any, Optional


@dataclass
class TimeWindow:
    start: datetime
    end: datetime


@dataclass
class Dimension:
    name: str
    value: str


@dataclass
class MetricDatapoint:
    timestamp: datetime
    average: Optional[float] = None
    sum_: Optional[float] = None
    sample_count: Optional[float] = None
    minimum: Optional[float] = None
    maximum: Optional[float] = None


def parse_datapoints(raw_data: List[Dict[str, Any]]) -> List[MetricDatapoint]:
    points = []
    for item in raw_data:
        points.append(
            MetricDatapoint(
                timestamp=item["Timestamp"],
                average=item.get("Average"),
                sum_=item.get("Sum"),
                sample_count=item.get("SampleCount"),
                minimum=item.get("Minimum"),
                maximum=item.get("Maximum"),
            )
        )
    return points
