import datetime
from typing import List, Tuple, Dict
from google.cloud import monitoring_v3
from observability_client import MonitoringClient
from observability_models import MetricFilter, MetricSeries, MetricDataPoint


def compare_metric_series(
    metric_type: str,
    end_time: datetime.datetime,
    start_time: datetime.datetime,
    interval_seconds: int,
    filter1_labels: Dict[str, str],
    filter2_labels: Dict[str, str],
) -> Tuple[MetricSeries, MetricSeries]:
    client = MonitoringClient()
    metric_service_client = client.get_metric_service_client()
    project_name = client.get_project_name()

    interval = monitoring_v3.TimeInterval(
        end_time=end_time.timestamp(),
        start_time=start_time.timestamp(),
    )

    aggregation = monitoring_v3.Aggregation(
        alignment_period={"seconds": interval_seconds},
        per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
    )

    def _fetch_series(labels: Dict[str, str]) -> List[MetricDataPoint]:
        filters = [f'metric.type="{metric_type}"']
        for label_key, label_value in labels.items():
            filters.append(f'resource.labels.{label_key}="{label_value}"')
        full_filter = " AND ".join(filters)

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

    series1_datapoints = _fetch_series(filter1_labels)
    series2_datapoints = _fetch_series(filter2_labels)

    series1 = MetricSeries(
        metric_type=metric_type,
        data_points=series1_datapoints,
        resource_labels=filter1_labels,
    )
    series2 = MetricSeries(
        metric_type=metric_type,
        data_points=series2_datapoints,
        resource_labels=filter2_labels,
    )

    return series1, series2
