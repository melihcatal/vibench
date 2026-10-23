import os
from datetime import datetime, timedelta
from google.cloud import monitoring_v3
from observability_client import get_monitoring_client
from observability_models import AggregatedMetric


def aggregate_metric_stats(
    project_id: str,
    metric_type: str,
    minutes_ago: int = 60,
    reducer: monitoring_v3.types.Aggregation.Reducer = monitoring_v3.types.Aggregation.Reducer.REDUCE_MEAN,
) -> List[AggregatedMetric]:
    client = get_monitoring_client()
    project_name = f"projects/{project_id}"

    now = datetime.utcnow()
    end_time = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    start_time = (now - timedelta(minutes=minutes_ago)).strftime("%Y-%m-%dT%H:%M:%SZ")

    interval = monitoring_v3.TimeInterval(
        end_time={
            "seconds": int(
                datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%SZ").timestamp()
            )
        },
        start_time={
            "seconds": int(
                datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%SZ").timestamp()
            )
        },
    )

    aggregation = monitoring_v3.Aggregation(
        alignment_period={"seconds": 300},  # 5 minutes alignment
        per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
        cross_series_reducer=reducer,
        group_by_fields=[],  # Aggregate across all series for overall stats
    )

    results = client.list_time_series(
        name=project_name,
        filter=f'metric.type = "{metric_type}"',
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        aggregation=aggregation,
    )

    aggregated_data = []
    for series in results:
        for point in series.points:
            value = (
                point.value.double_value
                or point.value.int6_4_value
                or point.value.bool_value
            )
            aggregated_data.append(
                AggregatedMetric(
                    interval_start=str(point.interval.start),
                    interval_end=str(point.interval.end),
                    value=value,
                    reducer=monitoring_v3.types.Aggregation.Reducer(reducer).name,
                )
            )
    return aggregated_data
