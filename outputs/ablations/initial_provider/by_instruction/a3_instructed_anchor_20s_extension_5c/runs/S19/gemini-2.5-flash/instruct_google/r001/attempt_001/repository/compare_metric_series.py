from google.cloud import monitoring_v3
from observability_client import get_metrics_client
from observability_models import MetricQuery, MetricDatapoint, MetricQueryResult
from typing import List


def compare_metric_series(
    query1: MetricQuery, query2: MetricQuery
) -> List[MetricQueryResult]:
    client = get_metrics_client()
    project_name = f"projects/{query1.project_id}"

    def _get_series(query: MetricQuery) -> MetricQueryResult:
        interval = monitoring_v3.TimeInterval(
            start_time={'seconds': int(query.interval_start_time)},
            end_time={'seconds': int(query.interval_end_time)},
        )

        filter_string = f'metric.type = "{query.metric_type}"'
        for f in query.filters:
            filter_string += f' AND {f}'

        aggregation = monitoring_v3.Aggregation(
            alignment_period={'seconds': int(query.period.rstrip('s'))},
            per_series_aligner=getattr(
                monitoring_v3.Aggregation.Aligner, query.aligner
            ),
            cross_series_reducer=getattr(
                monitoring_v3.Aggregation.Reducer, query.reducer
            ),
            group_by_fields=query.filters,
        )

        results = client.list_time_series(
            name=project_name,
            filter=filter_string,
            interval=interval,
            view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            aggregation=aggregation,
        )

        datapoints = []
        metric_name = query.metric_type

        for series in results:
            metric_name = series.metric.type
            for point in series.points:
                timestamp = point.interval.end_time.seconds
                value = point.value.double_value or point.value.int64_value
                labels = dict(series.metric.labels)
                datapoints.append(MetricDatapoint(str(timestamp), value, labels))
        return MetricQueryResult(metric_name, datapoints)

    series1 = _get_series(query1)
    series2 = _get_series(query2)

    return [series1, series2]
