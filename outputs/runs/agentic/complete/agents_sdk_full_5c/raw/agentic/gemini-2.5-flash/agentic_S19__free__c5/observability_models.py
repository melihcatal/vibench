from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
import datetime

@dataclass
class TimeSeriesPointValue:
    double_value: Optional[float] = None
    int64_value: Optional[int] = None
    string_value: Optional[str] = None
    bool_value: Optional[bool] = None

@dataclass
class TimeSeriesPointInterval:
    start_time: str # ISO format
    end_time: str # ISO format

@dataclass
class TimeSeriesPoint:
    interval: TimeSeriesPointInterval
    value: TimeSeriesPointValue

@dataclass
class Metric:
    type: str
    labels: Dict[str, str] = field(default_factory=dict)

@dataclass
class MonitoredResource:
    type: str
    labels: Dict[str, str] = field(default_factory=dict)

@dataclass
class TimeSeriesData:
    metric: Metric
    resource: MonitoredResource
    points: List[TimeSeriesPoint] = field(default_factory=list)

@dataclass
class MetricQueryResponse:
    time_series: List[TimeSeriesData] = field(default_factory=list)

def parse_time_series_response(response: Any) -> MetricQueryResponse:
    """Parses a Google Cloud Monitoring ListTimeSeriesResponse into a structured object."""
    parsed_series = []
    for series in response:
        metric = Metric(type=series.metric.type, labels=dict(series.metric.labels))
        resource = MonitoredResource(type=series.resource.type, labels=dict(series.resource.labels))
        
        points = []
        for p in series.points:
            interval = TimeSeriesPointInterval(
                start_time=p.interval.start_time.isoformat(),
                end_time=p.interval.end_time.isoformat()
            )
            value_dict = dict(p.value)
            point_value = TimeSeriesPointValue()
            if 'double_value' in value_dict:
                point_value.double_value = value_dict['double_value']
            elif 'int64_value' in value_dict:
                point_value.int64_value = value_dict['int64_value']
            elif 'string_value' in value_dict:
                point_value.string_value = value_dict['string_value']
            elif 'bool_value' in value_dict:
                point_value.bool_value = value_dict['bool_value']
            
            points.append(TimeSeriesPoint(interval=interval, value=point_value))
        
        parsed_series.append(TimeSeriesData(metric=metric, resource=resource, points=points))
    
    return MetricQueryResponse(time_series=parsed_series)
