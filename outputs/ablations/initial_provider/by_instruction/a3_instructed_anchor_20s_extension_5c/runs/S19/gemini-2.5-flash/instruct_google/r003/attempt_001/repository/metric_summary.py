from google.cloud import aiplatform
from observability_models import MetricResponse, TimeSeries, TimeSeriesPoint
from typing import List, Dict
from vertexai.language_models import TextGenerationModel

def summarize_metric_trends(project_id: str, region: str, metric_response: MetricResponse) -> str:
    aiplatform.init(project=project_id, location=region)
    model = TextGenerationModel.from_pretrained("text-bison@001")

    metric_data_str = ""
    for ts in metric_response.time_series:
        metric_data_str += f"Metric Labels: {ts.metric_labels}, Resource Labels: {ts.resource_labels}\n"
        for point in ts.points:
            metric_data_str += f"  Timestamp: {point.timestamp}, Value: {point.value}\n"
    
    prompt = f"Summarize the following metric data and identify any significant trends or anomalies:\n\n{metric_data_str}"

    response = model.predict(
        prompt,
        temperature=0.2,
        max_output_tokens=1024,
    )
    return response.text