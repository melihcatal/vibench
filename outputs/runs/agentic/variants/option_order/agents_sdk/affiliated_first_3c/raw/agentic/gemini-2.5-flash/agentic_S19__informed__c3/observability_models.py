from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional

@dataclass
class PointValue:
    int64_value: Optional[int] = None
    double_value: Optional[float] = None
    string_value: Optional[str] = None
    bool_value: Optional[bool] = None

    @classmethod
    def from_monitoring_value(cls, value) -> 'PointValue':
        if value.HasField('int64_value'):
            return cls(int64_value=value.int64_value)
        if value.HasField('double_value'):
            return cls(double_value=value.double_value)
        if value.HasField('string_value'):
            return cls(string_value=value.string_value)
        if value.HasField('bool_value'):
            return cls(bool_value=value.bool_value)
        return cls() # Return empty if no known field

@dataclass
class TimeInterval:
    start_time: datetime
    end_time: datetime

    @classmethod
    def from_monitoring_interval(cls, interval) -> 'TimeInterval':
        return cls(
            start_time=datetime.fromtimestamp(interval.start_time.seconds),
            end_time=datetime.fromtimestamp(interval.end_time.seconds),
        )

@dataclass
class MetricPoint:
    value: PointValue
    interval: TimeInterval

    @classmethod
    def from_monitoring_point(cls, point) -> 'MetricPoint':
        return cls(
            value=PointValue.from_monitoring_value(point.value),
            interval=TimeInterval.from_monitoring_interval(point.interval),
        )

@dataclass
class ResourceLabels:
    type: str
    labels: Dict[str, str]

    @classmethod
    def from_monitoring_resource(cls, resource) -> 'ResourceLabels':
        return cls(
            type=resource.type,
            labels=dict(resource.labels)
        )

@dataclass
class TimeSeriesData:
    resource: ResourceLabels
    metric_kind: str
    value_type: str
    points: List[MetricPoint]

    @classmethod
    def from_monitoring_time_series(cls, ts) -> 'TimeSeriesData':
        return cls(
            resource=ResourceLabels.from_monitoring_resource(ts.resource),
            metric_kind=ts.metric_kind.name,
            value_type=ts.value_type.name,
            points=[MetricPoint.from_monitoring_point(p) for p in ts.points]
        )

@dataclass
class MetricQuery:
    project_id: str
    metric_type: str
    end_time: datetime
    duration_minutes: int
    filter_string: Optional[str] = None
    aggregator_type: Optional[str] = None
    reducer_type: Optional[str] = None
    group_by_fields: List[str] = field(default_factory=list)


if __name__ == '__main__':
    # Example of how to use these models (requires a mock/real Google Cloud Monitoring TimeSeries object)
    # from google.cloud import monitoring_v3
    # from google.protobuf.timestamp_pb2 import Timestamp

    # # Mock a TimeSeries object for demonstration
    # mock_timestamp_end = Timestamp(seconds=int(datetime.now().timestamp()))
    # mock_timestamp_start = Timestamp(seconds=int((datetime.now() - timedelta(minutes=5)).timestamp()))

    # mock_point = monitoring_v3.Point(
    #     interval=monitoring_v3.TimeInterval(end_time=mock_timestamp_end, start_time=mock_timestamp_start),
    #     value=monitoring_v3.TypedValue(int64_value=123)
    # )
    # mock_resource = monitoring_v3.MonitoredResource(type="gce_instance", labels={"instance_id": "1234", "zone": "us-central1-a"})

    # mock_time_series = monitoring_v3.TimeSeries(
    #     metric_kind=monitoring_v3.MetricDescriptor.MetricKind.GAUGE,
    #     value_type=monitoring_v3.MetricDescriptor.ValueType.INT64,
    #     resource=mock_resource,
    #     points=[mock_point]
    # )

    # normalized_data = TimeSeriesData.from_monitoring_time_series(mock_time_series)

    # print(f"Normalized Resource Type: {normalized_data.resource.type}")
    # print(f"Normalized Metric Kind: {normalized_data.metric_kind}")
    # if normalized_data.points:
    #     print(f"First Point Value: {normalized_data.points[0].value.int64_value}")
    #     print(f"First Point End Time: {normalized_data.points[0].interval.end_time}")
    pass
