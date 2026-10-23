
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, List

@dataclass
class TimeSeriesPoint:
    """Represents a single data point in a time series."""
    timestamp: datetime
    value: Any

@dataclass
class MetricTimeSeries:
    """Represents a full time series with its metadata and data points."""
    metric_kind: str
    value_type: str
    labels: Dict[str, str]
    points: List[TimeSeriesPoint]

def parse_time_series_response(response) -> List[MetricTimeSeries]:
    """Parses a 'list_time_series' API response into a list of dataclasses."""
    results = []
    for series in response:
        points = []
        for point in series.points:
            points.append(
                TimeSeriesPoint(
                    timestamp=point.interval.end_time.timestamp(),
                    value=point.value.double_value or point.value.int64_value
                )
            )
        
        results.append(
            MetricTimeSeries(
                metric_kind=str(series.metric_kind),
                value_type=str(series.value_type),
                labels={label: value for label, value in series.metric.labels.items()},
                points=points
            )
        )
    return results
