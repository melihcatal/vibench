import json

from google.cloud import monitoring_v3

def aggregate_metric_stats(payload, config=None):
    config = config or {}
    client = monitoring_v3.MetricServiceClient()
    series = client.list_time_series(request={"name": f"projects/{config['project_id']}",
        "filter": "metric.type = " + json.dumps(payload["metric"]),
        "interval": {"start_time": {"seconds": int(payload["start_time"])},
                       "end_time": {"seconds": int(payload["end_time"])}},
        "aggregation": {"alignment_period": {"seconds": config.get("period_seconds", 60)},
                          "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN},
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL})
    stats = client.aggregate_time_series(request={"name": f"projects/{config['project_id']}",
        "filter": "metric.type = " + json.dumps(payload["metric"]),
        "interval": {"start_time": {"seconds": int(payload["start_time"])},
                       "end_time": {"seconds": int(payload["end_time"])}},
        "aggregation": {"alignment_period": {"seconds": config.get("period_seconds", 60)},
                          "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN},
        "view": monitoring_v3.AggregateTimeSeriesRequest.View.FULL})
    return {"stats": stats}