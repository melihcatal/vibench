import datetime
from typing import List
from google.cloud import monitoring_v3
from observability_client import MonitoringClient
from observability_models import MetricQuery, MetricDataPoint


def query_metric_window(query: MetricQuery) -> List[MetricDataPoint]:
    client = MonitoringClient()
    metric_service_client = client.get_metric_service_client()
    project_name = client.get_project_name()

    interval = monitoring_v3.TimeInterval(
        end_time=query.end_time.timestamp(),
        start_time=query.start_time.timestamp(),
    )

    # Using a simple aggregation to get raw data points
    aggregation = monitoring_v3.Aggregation(
        alignment_period={"seconds": query.interval_seconds},
        per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,  # ALIGN_NONE can also be used for raw data, but ALIGN_MEAN provides a value
    )

    results = metric_service_client.list_time_series(
        name=project_name,
        filter=f'metric.type="{query.metric_type}"',
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        aggregation=aggregation,
    )

    datapoints = []
    for series in results:
        for point in series.points:
            datapoints.append(
                MetricDataPoint(
                    timestamp=datetime.datetime.fromtimestamp(
                        point.interval.end_time.seconds
                    ),
                    value=point.value.double_value
                    or point.value.int64_value
                    or point.value.distribution_value.mean,
                    labels=dict(series.resource.labels),
                )
            )
    return datapoints
