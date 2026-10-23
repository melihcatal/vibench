import json
import textwrap

from google.cloud import monitoring_v3

from observability_client import get_monitoring_client, get_generative_model
from observability_models import MetricPoint

def metric_summary(payload, config=None):
    config = config or {}
    monitoring_client = get_monitoring_client()
    generative_model = get_generative_model()

    metric_type = payload["metric"]
    start_time = payload["start_time"]
    end_time = payload["end_time"]
    project_id = config["project_id"]
    period_seconds = config.get("period_seconds", 60)

    # Fetch metric data
    series_data = monitoring_client.list_time_series(request={
        "name": f"projects/{project_id}",
        "filter": f"metric.type = {json.dumps(metric_type)}",
        "interval": {
            "start_time": {"seconds": int(start_time)}
            ,
            "end_time": {"seconds": int(end_time)}
        },
        "aggregation": {
            "alignment_period": {"seconds": period_seconds},
            "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN
        },
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL
    })

    points = []
    for timeseries in series_data:
        for point in timeseries.points:
            kind = point.value._pb.WhichOneof("value")
            if kind not in ("double_value", "int64_value"):
                raise ValueError("Expected a scalar numeric metric")
            points.append(MetricPoint(timestamp=point.interval.end_time.timestamp(), value=float(getattr(point.value, kind))))
    
    # Prepare data for summary
    data_for_summary = ""
    if points:
        data_for_summary = "Metric points (timestamp, value):\n"
        for p in sorted(points, key=lambda p: p.timestamp):
            data_for_summary += f"- {p.timestamp}: {p.value}\n"
    else:
        data_for_summary = "No data points found for the given metric and time window."

    # Generate summary using the generative model
    prompt = textwrap.dedent(f"""
    Analyze the following metric data and provide a concise summary of trends or anomalies. 
    If no data is present, state that. 
    Metric Type: {metric_type}
    Start Time: {start_time}
    End Time: {end_time}

    {data_for_summary}

    Summary:
    """)
    
    response = generative_model.generate_content(prompt)
    summary = response.text

    return {"metric_summary": summary}
