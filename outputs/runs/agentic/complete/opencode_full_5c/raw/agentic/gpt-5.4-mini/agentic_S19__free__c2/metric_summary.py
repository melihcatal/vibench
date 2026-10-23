from google.api_core import datetime_helpers
from google.cloud import monitoring_v3

from observability_client import (
    load_config,
    monitoring_client,
    project_name,
    normalize_metric_name,
)


def metric_summary(metric_type, start_time, end_time):
    config = load_config()
    client = monitoring_client()
    interval = {
        "start_time": datetime_helpers.to_datetime(start_time),
        "end_time": datetime_helpers.to_datetime(end_time),
    }
    aggregation = monitoring_v3.Aggregation(
        alignment_period={"seconds": 300},
        per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
    )
    results = list(
        client.list_time_series(
            name=project_name(config),
            filter=f'metric.type="{normalize_metric_name(metric_type, config)}"',
            interval=interval,
            aggregation=aggregation,
            view=monitoring_client().TimeSeriesView.FULL,
        )
    )
    return {
        "metric_type": metric_type,
        "points": len(results),
        "series": [
            getattr(r, "metric", None).labels if getattr(r, "metric", None) else {}
            for r in results
        ],
    }
