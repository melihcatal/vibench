from google.cloud import monitoring_v3
from datetime import datetime, timedelta

def metric_summary(payload, project_id):
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    now = datetime.utcnow()
    end_time = now
    start_time = now - timedelta(minutes=payload.get("window_minutes", 60))

    interval = monitoring_v3.TimeInterval(
        end_time={'seconds': int(end_time.timestamp())},
        start_time={'seconds': int(start_time.timestamp())}
    )

    query_params = {
        "name": project_name,
        "filter": f'metric.type = "{payload["metric_type"]}" ' \
                  f'AND resource.type = "{payload["resource_type"]}"',
        "interval": interval,
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    }

    # Add aggregation if specified in payload
    if "aggregation" in payload:
        aggregation = monitoring_v3.Aggregation(
            alignment_period={'seconds': payload["aggregation"].get("period_seconds", 300)},
            per_series_aligner=getattr(monitoring_v3.Aggregation.Aligner, payload["aggregation"].get("aligner", "ALIGN_MEAN"))
        )
        query_params["aggregation"] = aggregation

    response = client.list_time_series(**query_params)

    summary_data = []
    for series in response:
        for point in series.points:
            value = point.value.double_value if point.value.HasField('double_value') else None
            if value is not None:
                summary_data.append(value)

    if not summary_data:
        return {"summary": "No data available for the specified metric and time window."}

    min_val = min(summary_data)
    max_val = max(summary_data)
    avg_val = sum(summary_data) / len(summary_data)

    return {
        "summary": f"Metric {payload['metric_type']} over last {payload.get('window_minutes', 60)} minutes:",
        "min_value": min_val,
        "max_value": max_val,
        "average_value": avg_val,
    }
