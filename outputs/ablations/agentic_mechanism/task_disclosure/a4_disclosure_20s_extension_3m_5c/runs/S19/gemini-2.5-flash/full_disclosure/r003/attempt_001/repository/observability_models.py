from dataclasses import dataclass
from typing import List, Dict, Any, Optional

@dataclass
class MetricDataPoint:
    timestamp: str
    value: float

@dataclass
class MetricSeries:
    metric_name: str
    resource_labels: Dict[str, str]
    metric_labels: Dict[str, str]
    points: List[MetricDataPoint]

@dataclass
class MetricRequest:
    metric_name: str
    start_time: str
    end_time: str
    interval: str
    filters: Optional[Dict[str, str]] = None
    dimensions: Optional[List[str]] = None

@dataclass
class MetricResponse:
    metric_series: List[MetricSeries]
    query_time: str
    
def normalize_metric_data(raw_data: Dict[str, Any]) -> List[MetricSeries]:
    """
    Normalizes raw metric data into a list of MetricSeries objects.
    This is a placeholder function and should be implemented based on the specific
    structure of the raw data from the monitoring service.
    """
    normalized_series = []
    # Example placeholder for normalization logic
    # In a real scenario, this would parse the raw_data
    # from a specific monitoring API response format
    # and transform it into the MetricSeries structure.
    # For now, we'll return an empty list or a very basic structure.
    
    if raw_data and "series" in raw_data:
        for series_data in raw_data["series"]:
            points = [MetricDataPoint(timestamp=p["timestamp"], value=p["value"]) for p in series_data.get("points", [])]
            normalized_series.append(MetricSeries(
                metric_name=series_data.get("metric_name", "unknown"),
                resource_labels=series_data.get("resource_labels", {}),
                metric_labels=series_data.get("metric_labels", {}),
                points=points
            ))
            
    return normalized_series
