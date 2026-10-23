import dataclasses
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

@dataclasses.dataclass
class Label:
    key: str
    value: str

@dataclasses.dataclass
class Metric:
    name: str
    labels: Optional[List[Label]] = None

@dataclasses.dataclass
class Datapoint:
    timestamp: datetime
    value: Union[int, float]

@dataclasses.dataclass
class TimeSeries:
    metric: Metric
    points: List[Datapoint]

@dataclasses.dataclass
class QueryRequest:
    metric_name: str
    start_time: datetime
    end_time: datetime
    interval_seconds: Optional[int] = None
    filters: Optional[Dict[str, str]] = None

@dataclasses.dataclass
class QueryResponse:
    time_series: List[TimeSeries]

def normalize_time_series(
    series_list: List[TimeSeries],
    start_time: datetime,
    end_time: datetime,
    interval_seconds: int,
    fill_value: Union[int, float, None] = None
) -> List[TimeSeries]:
    """
    Normalizes a list of TimeSeries to a common time window and interval.
    Missing data points within the window are filled with fill_value.
    """
    normalized_series_list = []
    
    for series in series_list:
        normalized_points: List[Datapoint] = []
        current_time = start_time
        series_points_map = {dp.timestamp: dp.value for dp in series.points}

        while current_time <= end_time:
            value = series_points_map.get(current_time, fill_value)
            if value is not None:
                normalized_points.append(Datapoint(timestamp=current_time, value=value))
            current_time = current_time + timedelta(seconds=interval_seconds)
        
        normalized_series_list.append(TimeSeries(metric=series.metric, points=normalized_points))
    
    return normalized_series_list

from datetime import timedelta
