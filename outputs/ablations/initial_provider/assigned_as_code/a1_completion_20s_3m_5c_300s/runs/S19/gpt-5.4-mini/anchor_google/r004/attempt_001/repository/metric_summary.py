from google.cloud import monitoring_v3

from observability_client import load_config, metric_client, project_name
from observability_models import build_time_window, extract_scalar_value


def metric_summary(payload, config=None):
    cfg = load_config(config)
    client = metric_client()
    series = client.list_time_series(request={"name": project_name(cfg),
        "filter": f'metric.type = "{payload["metric"]}"',
        "interval": build_time_window(payload),
        "aggregation": {"alignment_period": {"seconds": cfg.period_seconds},
                        "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN},
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL})
    values = []
    for timeseries in series:
        for point in timeseries.points:
            values.append(extract_scalar_value(point))
    if not values:
        return {"trend": "no_data", "anomaly": False}
    delta = values[-1] - values[0] if len(values) > 1 else 0.0
    return {"trend": "rising" if delta > 0 else "falling" if delta < 0 else "flat", "anomaly": abs(delta) > (sum(values) / len(values) if values else 0)}
