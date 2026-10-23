from google.api_core import datetime_helpers
from google.cloud import monitoring_v3

from observability_client import (
    load_config,
    monitoring_client,
    project_name,
    normalize_metric_name,
)
from observability_models import MetricAggregateRequest, series_to_list


def aggregate_metric_stats(
    metric_type,
    start_time,
    end_time,
    alignment_period_seconds=60,
    reducer="REDUCE_MEAN",
):
    config = load_config()
    client = monitoring_client()
    request = MetricAggregateRequest(
        metric_type=normalize_metric_name(metric_type, config),
        start_time=start_time,
        end_time=end_time,
        alignment_period_seconds=alignment_period_seconds,
        reducer=reducer,
    )
    interval = {
        "start_time": datetime_helpers.to_datetime(request.start_time),
        "end_time": datetime_helpers.to_datetime(request.end_time),
    }
    aggregation = monitoring_v3.Aggregation(
        alignment_period={"seconds": request.alignment_period_seconds},
        per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
        cross_series_reducer=getattr(
            monitoring_v3.Aggregation.Reducer, request.reducer
        ),
    )
    results = client.list_time_series(
        name=project_name(config),
        filter=f'metric.type="{request.metric_type}"',
        interval=interval,
        aggregation=aggregation,
        view=monitoring_client().TimeSeriesView.FULL,
    )
    return series_to_list(list(results))
