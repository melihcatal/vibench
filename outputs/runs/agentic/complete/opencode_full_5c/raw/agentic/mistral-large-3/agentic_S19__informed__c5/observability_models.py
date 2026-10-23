from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass
from datetime import datetime


@dataclass
class MetricQuery:
    metric_type: str
    hours: int = 1
    resource_labels: Optional[Dict[str, str]] = None
    filter_str: Optional[str] = None


@dataclass
class MetricDatapoint:
    timestamp: datetime
    value: float
    labels: Dict[str, str]


@dataclass
class MetricResponse:
    metric_type: str
    datapoints: List[MetricDatapoint]

    @classmethod
    def from_gcp_time_series(cls, time_series) -> "MetricResponse":
        datapoints = []
        for series in time_series:
            for point in series.points:
                datapoints.append(
                    MetricDatapoint(
                        timestamp=datetime.fromtimestamp(
                            point.interval.end_time.timestamp()
                        ),
                        value=float(point.value.double_value),
                        labels=dict(series.resource.labels),
                    )
                )
        return cls(metric_type=time_series[0].metric.type, datapoints=datapoints)


@dataclass
class AggregatedMetricResponse:
    metric_type: str
    aggregation: str
    value: float

    @classmethod
    def from_gcp_time_series(cls, time_series) -> "AggregatedMetricResponse":
        for series in time_series:
            for point in series.points:
                return cls(
                    metric_type=series.metric.type,
                    aggregation="aggregated",
                    value=float(point.value.double_value),
                )
        raise ValueError("No aggregated data found")


@dataclass
class ComparisonResponse:
    metric_type: str
    series_a: List[MetricDatapoint]
    series_b: List[MetricDatapoint]

    @classmethod
    def from_gcp_time_series(cls, series_a, series_b) -> "ComparisonResponse":
        def extract_datapoints(series):
            datapoints = []
            for s in series:
                for point in s.points:
                    datapoints.append(
                        MetricDatapoint(
                            timestamp=datetime.fromtimestamp(
                                point.interval.end_time.timestamp()
                            ),
                            value=float(point.value.double_value),
                            labels=dict(s.resource.labels),
                        )
                    )
            return datapoints

        return cls(
            metric_type=series_a[0].metric.type,
            series_a=extract_datapoints(series_a),
            series_b=extract_datapoints(series_b),
        )
