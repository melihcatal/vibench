from datetime import datetime, timedelta, timezone
from google.cloud.monitoring_v3.types import ListTimeSeriesRequest, TimeInterval, Aggregation
from google.protobuf.timestamp_pb2 import Timestamp

from observability_client import get_monitoring_client, get_project_id
from observability_models import MetricTimeSeries, TimeSeriesPoint

def get_aggregated_metric(
    metric_type: str, 
    minutes_ago: int = 60,
    aligner: Aggregation.Aligner = Aggregation.Aligner.ALIGN_MEAN,
    reducer: Aggregation.Reducer = Aggregation.Reducer.REDUCE_SUM
) -> list[MetricTimeSeries]:
    """
    Retrieves aggregated statistics for a metric over a time window.
    
    :param metric_type: The metric to query.
    :param minutes_ago: The time window in minutes.
    :param aligner: The alignment function.
    :param reducer: The reduction function across time series.
    :return: A list of aggregated time series data.
    """
    client = get_monitoring_client()
    project_name = f"projects/{get_project_id()}"

    now = datetime.now(timezone.utc)
    start_time = now - timedelta(minutes=minutes_ago)
    
    interval = TimeInterval(
        start_time=Timestamp(seconds=int(start_time.timestamp())),
        end_time=Timestamp(seconds=int(now.timestamp()))
    )

    aggregation = Aggregation(
        alignment_period={"seconds": 60 * 5},  # 5 minute alignment period
        per_series_aligner=aligner,
        cross_series_reducer=reducer,
        group_by_fields=["metric.label.state", "resource.zone"],
    )

    request = ListTimeSeriesRequest(
        name=project_name,
        filter=f'metric.type = "{metric_type}"',
        interval=interval,
        view=ListTimeSeriesRequest.TimeSeriesView.FULL,
        aggregation=aggregation,
    )
    
    results = client.list_time_series(request=request)
    
    output = []
    for result in results:
        points = [
            TimeSeriesPoint(timestamp=p.interval.end_time.isoformat(), value=p.value.double_value)
            for p in result.points
        ]
        series = MetricTimeSeries(
            metric_kind=str(result.metric_kind),
            value_type=str(result.value_type),
            points=points,
            resource_labels=dict(result.resource.labels),
            metric_labels=dict(result.metric.labels),
        )
        output.append(series)

    return output
