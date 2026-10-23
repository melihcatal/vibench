import google.generativeai as genai
from google.cloud import monitoring_v3
import os
import datetime
from google.protobuf.timestamp_pb2 import Timestamp

def summarize_metric_trends(project_id: str, metric_type: str, end_time_iso: str, duration_seconds: int):
    monitoring_client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    end_dt = datetime.datetime.fromisoformat(end_time_iso.replace('Z', '+00:00'))
    end_time_timestamp = Timestamp()
    end_time_timestamp.FromDatetime(end_dt)

    start_time_timestamp = Timestamp()
    start_dt = end_dt - datetime.timedelta(seconds=duration_seconds)
    start_time_timestamp.FromDatetime(start_dt)

    interval = monitoring_v3.TimeInterval(
        end_time=end_time_timestamp,
        start_time=start_time_timestamp,
    )

    query = f'metric.type = "{metric_type}"'

    results = monitoring_client.list_time_series(
        request={
            "name": project_name,
            "filter": query,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )

    metric_data_str = []
    for series in results:
        if series.points:
            last_point = series.points[-1]
            value = next(iter(last_point.value.values())) if last_point.value else "N/A"
            metric_data_str.append(f"Metric: {series.metric.type}, Resource: {series.resource.type}, Latest Value: {value}")
    
    if not metric_data_str:
        return "No metric data found for summarization."

    model = genai.GenerativeModel('gemini-pro') # Provider-specific model ID
    prompt = f"Summarize the recent trend or anomalies from the following metric data:\n\n{'\\n'.join(metric_data_str)}\n\nProvide a concise summary of significant observations."
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error summarizing with Gemini: {e}"
