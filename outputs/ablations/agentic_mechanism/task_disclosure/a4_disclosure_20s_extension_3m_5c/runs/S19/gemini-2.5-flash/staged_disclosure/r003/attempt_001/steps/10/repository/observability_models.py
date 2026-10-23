
"""
Local request, response, and normalization helpers for Managed Metrics Monitoring.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union

@dataclass
class MetricRequest:
    """Represents a request for metric data."""
    metric_name: str
    start_time: str
    end_time: str
    dimensions: Optional[Dict[str, str]] = field(default_factory=dict)
    filters: Optional[Dict[str, Any]] = field(default_factory=dict)
    period: Optional[int] = None # in seconds

@dataclass
class MetricDataPoint:
    """Represents a single data point for a metric."""
    timestamp: str
    value: Union[float, int]
    unit: Optional[str] = None

@dataclass
class MetricResponse:
    """Represents a response containing metric data."""
    metric_name: str
    data_points: List[MetricDataPoint] = field(default_factory=list)
    dimensions: Optional[Dict[str, str]] = field(default_factory=dict)
    status: str = "success"
    message: Optional[str] = None

def normalize_metric_data(
    raw_data: Dict[str, Any],
    service_provider: str
) -> MetricResponse:
    """
    Normalizes raw metric data from various service providers into a common MetricResponse format.

    Args:
        raw_data: The raw metric data from a specific monitoring service.
        service_provider: The name of the service provider (e.g., "aws_cloudwatch", "google_cloud_monitoring").

    Returns:
        A MetricResponse object containing the normalized metric data.
    """
    normalized_data = MetricResponse(metric_name="unknown")

    if service_provider == "aws_cloudwatch":
        # Example normalization for AWS CloudWatch (simplified)
        # In a real scenario, this would parse CloudWatch GetMetricData output
        label = raw_data.get('Label', 'unknown_metric')
        timestamps = raw_data.get('Timestamps', [])
        values = raw_data.get('Values', [])
        unit = raw_data.get('Unit')

        normalized_data.metric_name = label
        for i in range(len(timestamps)):
            if i < len(values):
                normalized_data.data_points.append(
                    MetricDataPoint(
                        timestamp=timestamps[i].isoformat() if hasattr(timestamps[i], 'isoformat') else str(timestamps[i]),
                        value=values[i],
                        unit=unit
                    )
                )
        normalized_data.status = "success" if normalized_data.data_points else "no_data"

    elif service_provider == "google_cloud_monitoring":
        # Example normalization for Google Cloud Monitoring (simplified)
        # In a real scenario, this would parse Google Cloud Monitoring time series data
        display_name = raw_data.get('displayName', 'unknown_metric')
        points = raw_data.get('points', []) # This would be from a TimeSeries object

        normalized_data.metric_name = display_name
        for point in points:
            interval = point.get('interval', {})
            value = point.get('value', {})
            # Assuming 'endTime' is the timestamp for the value
            timestamp = interval.get('endTime')

            if timestamp and value:
                # Extract the actual value, assuming it's a double or int value
                metric_value = value.get('doubleValue') or value.get('int64Value')
                if metric_value is not None:
                    normalized_data.data_points.append(
                        MetricDataPoint(
                            timestamp=timestamp,
                            value=metric_value
                        )
                    )
        normalized_data.status = "success" if normalized_data.data_points else "no_data"

    else:
        normalized_data.status = "error"
        normalized_data.message = f"Unsupported service provider: {service_provider}"

    return normalized_data
