from dataclasses import dataclass, field
from typing import List, Dict, Union, Any
from google.protobuf.timestamp_pb2 import Timestamp

@dataclass
class TimeSeriesPoint:
    """Represents a single data point in a time series."""
    timestamp: Timestamp
    value: Union[float, int]

@dataclass
class MetricSeries:
    """Represents a full time series with its metadata."""
    metric_kind: str
    value_type: str
    resource_labels: Dict[str, str]
    metric_labels: Dict[str, str]
    points: List[TimeSeriesPoint] = field(default_factory=list)

def to_metric_series_list(time_series_results: Any) -> List[MetricSeries]:
    """Converts Google Cloud Monitoring API results to a list of MetricSeries objects."""
    series_list = []
    for series in time_series_results:
        points = [
            TimeSeriesPoint(timestamp=p.interval.end_time, value=p.value.double_value or p.value.int64_value)
            for p in series.points
        ]
        ms = MetricSeries(
            metric_kind=str(series.metric_kind),
            value_type=str(series.value_type),
            resource_labels={label: value for label, value in series.resource.labels.items()},
            metric_labels={label: value for label, value in series.metric.labels.items()},
            points=points
        )
        series_list.append(ms)
    return series_list
