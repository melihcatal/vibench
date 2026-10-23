from typing import Dict, List, Optional, Union, Any
from datetime import datetime
from dataclasses import dataclass


@dataclass
class MetricDatapoint:
    """Represents a single datapoint for a metric."""

    timestamp: datetime
    value: float
    unit: str


@dataclass
class MetricStats:
    """Represents aggregated statistics for a metric."""

    average: Optional[float]
    sum: Optional[float]
    minimum: Optional[float]
    maximum: Optional[float]
    sample_count: int


@dataclass
class MetricQueryRequest:
    """Represents a request to query metric data."""

    metric_name: str
    namespace: str
    start_time: datetime
    end_time: datetime
    dimensions: Optional[List[Dict[str, str]]] = None
    statistics: Optional[List[str]] = None


def normalize_metric_response(response: Dict) -> List[MetricDatapoint]:
    """
    Normalize a CloudWatch get_metric_statistics response into a list of MetricDatapoint objects.

    Args:
        response: Response from CloudWatch get_metric_statistics API.

    Returns:
        List of MetricDatapoint objects.
    """
    datapoints = []
    for point in response.get("Datapoints", []):
        datapoints.append(
            MetricDatapoint(
                timestamp=point["Timestamp"],
                value=point.get("Average", 0.0),
                unit=point.get("Unit", "None"),
            )
        )

    return sorted(datapoints, key=lambda x: x.timestamp)


def normalize_metric_stats(response: Dict) -> MetricStats:
    """
    Normalize a CloudWatch get_metric_statistics response into a MetricStats object.

    Args:
        response: Response from CloudWatch get_metric_statistics API.

    Returns:
        MetricStats object.
    """
    if not response.get("Datapoints"):
        return MetricStats(
            average=None, sum=None, minimum=None, maximum=None, sample_count=0
        )

    latest_datapoint = max(response["Datapoints"], key=lambda x: x["Timestamp"])
    return MetricStats(
        average=latest_datapoint.get("Average"),
        sum=latest_datapoint.get("Sum"),
        minimum=latest_datapoint.get("Minimum"),
        maximum=latest_datapoint.get("Maximum"),
        sample_count=latest_datapoint.get("SampleCount", 0),
    )
