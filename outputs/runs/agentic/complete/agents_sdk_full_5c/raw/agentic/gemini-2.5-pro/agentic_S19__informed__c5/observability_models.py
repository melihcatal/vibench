from typing import TypedDict, List, Any

class TimeSeriesPoint(TypedDict):
    timestamp: str
    value: Any

class MetricSeries(TypedDict):
    metric_kind: str
    value_type: str
    points: List[TimeSeriesPoint]
    resource: dict

class FormattedMetricResponse(TypedDict):
    series: List[MetricSeries]
