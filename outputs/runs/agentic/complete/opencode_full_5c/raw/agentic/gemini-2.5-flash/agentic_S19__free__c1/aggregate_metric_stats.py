import os
from datetime import datetime, timedelta
from google.cloud import monitoring_v3


def aggregate_metric_stats(
    project_id: str,
    metric_type: str,
    window_minutes: int,
    aggregation_period_seconds: int,
):
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    now = datetime.utcnow()
    end_time = now
    start_time = now - timedelta(minutes=window_minutes)

    interval = monitoring_v3.TimeInterval(
        end_time={"seconds": int(end_time.timestamp())},
        start_time={"seconds": int(start_time.timestamp())},
    )

    aggregation = monitoring_v3.Aggregation(
        alignment_period={"seconds": aggregation_period_seconds},
        per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
        cross_series_reducer=monitoring_v3.Aggregation.Reducer.REDUCE_MEAN,
        group_by_fields=["metric.labels.instance_name"],
    )

    query_params = {
        "name": project_name,
        "filter": f'metric.type = "{metric_type}"',
        "interval": interval,
        "aggregation": aggregation,
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    }

    results = client.list_time_series(request=query_params)
    return [monitoring_v3.TimeSeries.to_dict(series) for series in results]
