from datetime import datetime, timedelta, timezone

from google.cloud import monitoring_v3

from observability_client import client, project_name


def aggregate_metric_stats(metric_type: str, minutes: int = 60, project_id: str | None = None):
    c = client()
    project = project_name(project_id)
    interval = monitoring_v3.TimeInterval(end_time=datetime.now(timezone.utc), start_time=datetime.now(timezone.utc) - timedelta(minutes=minutes))
    results = c.list_time_series(
        request={
            "name": project,
            "filter": f'metric.type = "{metric_type}"',
            "interval": interval,
            "aggregation": monitoring_v3.Aggregation(alignment_period={"seconds": minutes * 60}, per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_MEAN),
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )
    values = []
    for series in results:
        for point in series.points:
            if hasattr(point.value, "double_value"):
                values.append(point.value.double_value)
    return {"count": len(values), "mean": (sum(values) / len(values)) if values else None, "min": min(values) if values else None, "max": max(values) if values else None}
