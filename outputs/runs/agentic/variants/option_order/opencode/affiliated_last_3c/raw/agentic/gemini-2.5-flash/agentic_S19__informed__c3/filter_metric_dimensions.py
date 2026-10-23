import datetime
from typing import List
from google.cloud import monitoring_v3
from observability_client import MonitoringClient
from observability_models import MetricFilter, MetricDataPoint


def filter_metric_dimensions(metric_filter: MetricFilter) -> List[MetricDataPoint]:
    client = MonitoringClient()
    metric_service_client = client.get_metric_service_client()
    project_name = client.get_project_name()

    interval = monitoring_v3.TimeInterval(
        end_time=metric_filter.end_time.timestamp(),
        start_time=metric_filter.start_time.timestamp(),
    )

    filters = [f'metric.type="{metric_filter.metric_type}"']
    for label_key, label_value in metric_filter.resource_labels.items():
        filters.append(f'resource.labels.{label_key}="{label_value}"')

    full_filter = " AND ".join(filters)

    aggregation = monitoring_v3.Aggregation(
        alignment_period={"seconds": metric_filter.interval_seconds},
        per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
    )

    results = metric_service_client.list_time_series(
        name=project_name,
        filter=full_filter,
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
