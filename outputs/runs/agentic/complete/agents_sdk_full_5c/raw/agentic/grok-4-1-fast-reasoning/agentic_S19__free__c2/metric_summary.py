import os
from typing import List
import openai
from google.cloud import monitoring_v3
from observability_client import get_project_id
from observability_models import create_time_interval, build_metric_filter

def metric_summary(metric_name: str, window_minutes: int = 60) -> str:
    client = monitoring_v3.MetricServiceClient()
    project_id = get_project_id()
    interval = create_time_interval(window_minutes)
    filter_str = build_metric_filter(metric_name)
    request = {
        "name": f"projects/{project_id}",
        "filter": filter_str,
        "interval": interval,
        "view": "FULL",
    }
    values: List[float] = []
    for time_series in client.list_time_series(request):
        for point in time_series.points:
            value = getattr(point.value, 'double_value', 0.0) or getattr(point.value, 'int64_value', 0.0) or 0.0
            values.append(float(value))
    if not values:
        return "No metric data available."
    mean_val = sum(values) / len(values)
    data_str = f"Over last {window_minutes} minutes: {len(values)} datapoints, average {mean_val:.4f}, recent values: {values[-5:]}"
    openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Analyze metric data for trends, anomalies, increases, or decreases."},
            {"role": "user", "content": f"Summarize the metric '{metric_name}': {data_str}"}
        ],
        max_tokens=150
    )
    return response.choices[0].message.content
