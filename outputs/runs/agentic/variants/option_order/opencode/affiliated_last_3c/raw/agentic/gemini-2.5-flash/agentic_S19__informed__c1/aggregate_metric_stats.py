from google.cloud import monitoring_v3
from observability_client import get_monitoring_client, get_project_id
from observability_models import create_time_interval


def aggregate_metric_stats(metric_type, end_time_str, minutes, aggregator="MEAN"):
    client = get_monitoring_client()
    project_id = get_project_id()
    project_name = f"projects/{project_id}"
    interval = create_time_interval(end_time_str, minutes)

    query = f'metric.type="{metric_type}"'

    aggregation = monitoring_v3.Aggregation(
        alignment_period={"seconds": 60 * minutes},
        per_series_aligner=getattr(
            monitoring_v3.Aggregation.Aligner, f"ALIGN_{aggregator}"
        ),
        cross_series_reducer=monitoring_v3.Aggregation.Reducer.REDUCE_MEAN,
        group_by_fields=["metric.labels.instance_name"],
    )

    result = client.list_time_series(
        request={
            "name": project_name,
            "filter": query,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            "aggregation": aggregation,
        }
    )

    aggregated_data = []
    for ts in result:
        for point in ts.points:
            aggregated_data.append(
                {
                    "value": point.value.double_value or point.value.int64_value,
                    "timestamp": point.interval.end_time.isoformat(),
                    "metric_labels": {k: v for k, v in ts.metric.labels.items()},
                }
            )
    return aggregated_data
