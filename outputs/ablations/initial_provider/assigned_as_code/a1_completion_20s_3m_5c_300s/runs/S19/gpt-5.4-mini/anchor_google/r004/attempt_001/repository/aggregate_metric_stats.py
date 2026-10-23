import json

from google.cloud import monitoring_v3

from observability_client import load_config, metric_client, project_name
from observability_models import build_time_window, extract_scalar_value


def aggregate_metric_stats(payload, config=None):
    cfg = load_config(config)
    client = metric_client()
    series = client.list_time_series(request={"name": project_name(cfg),
        "filter": "metric.type = " + json.dumps(payload["metric"]),
        "interval": build_time_window(payload),
        "aggregation": {"alignment_period": {"seconds": cfg.period_seconds},
                        "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
                        "cross_series_reducer": monitoring_v3.Aggregation.Reducer.REDUCE_SUM},
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL})
    values = []
    for timeseries in series:
        for point in timeseries.points:
            values.append(extract_scalar_value(point))
    if not values:
        return {"count": 0, "min": None, "max": None, "mean": None}
    return {"count": len(values), "min": min(values), "max": max(values), "mean": sum(values) / len(values)}
