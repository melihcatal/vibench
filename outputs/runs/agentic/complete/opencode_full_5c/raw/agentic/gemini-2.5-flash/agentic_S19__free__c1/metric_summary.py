import os
from datetime import datetime, timedelta
from google.cloud import monitoring_v3


def summarize_metric_trends(project_id: str, metric_type: str, window_minutes: int):
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
        alignment_period={"seconds": 300},  # 5-minute alignment
        per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
        cross_series_reducer=monitoring_v3.Aggregation.Reducer.REDUCE_MEAN,
    )

    query_params = {
        "name": project_name,
        "filter": f'metric.type = "{metric_type}"',
        "interval": interval,
        "aggregation": aggregation,
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    }

    results = client.list_time_series(request=query_params)

    summary_data = []
    for series in results:
        points = [
            p.value.double_value
            for p in series.points
            if p.value.HasField("double_value")
        ]
        if points:
            summary_data.append(
                {
                    "metric": metric_type,
                    "min": min(points),
                    "max": max(points),
                    "average": sum(points) / len(points),
                }
            )
    return summary_data
