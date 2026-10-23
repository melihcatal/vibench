from google.cloud import monitoring_v3

from observability_client import load_observability_config, monitoring_client, project_name
from observability_models import normalize_aggregates


def aggregate_metric_stats(payload, config=None):
    config = load_observability_config(config)
    client = monitoring_client()
    series = client.list_time_series(request={"name": project_name(config), "filter": "metric.type = " + __import__("json").dumps(payload["metric"]), "interval": {"start_time": {"seconds": int(payload["start_time"])}, "end_time": {"seconds": int(payload["end_time"])}}, "aggregation": {"alignment_period": {"seconds": config.get("period_seconds", 60)}, "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN}, "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL})
    return normalize_aggregates(series)
