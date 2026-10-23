from dataclasses import dataclass
from typing import List, Optional
from google.cloud import aiplatform
from observability_models import TimeSeries

@dataclass
class MetricSummaryRequest:
    project_id: str
    location: str # e.g., us-central1
    metric_data: List[TimeSeries]

@dataclass
class MetricSummaryResponse:
    summary: str
    anomaly_detected: bool

def summarize_metric_trends(request: MetricSummaryRequest) -> MetricSummaryResponse:
    aiplatform.init(project=request.project_id, location=request.location)

    # For demonstration, we'll simulate a prompt based on the time series data
    # In a real scenario, you'd feed more sophisticated data points and context
    metric_info = []
    for ts in request.metric_data:
        metric_name = ts.metric_labels.get('metric_name', 'unknown_metric')
        resource_id = ts.resource_labels.get('resource_id', 'unknown_resource')
        values = [str(p.value) for p in ts.points]
        metric_info.append(f"Metric '{metric_name}' on resource '{resource_id}' has values: {', '.join(values[:10])}...")

    prompt_text = (f"Summarize the following metric trends and identify any anomalies:\n\n"
                   f"{'; '.join(metric_info)}\n\nSummary:")

    # Using a pre-trained text generation model from Vertex AI
    # Replace 'text-bison@001' with an appropriate model for summarization
    # For actual anomaly detection, a more complex model or rule-based system would be needed
    model = aiplatform.PredictionServiceClient(client_options={"api_endpoint": f"{request.location}-aiplatform.googleapis.com"})
    endpoint = f"projects/{request.project_id}/locations/{request.location}/publishers/google/models/text-bison@001"

    response = model.predict(
        endpoint=endpoint,
        instances=[{"prompt": prompt_text}],
        parameters={"temperature": 0.2, "maxOutputTokens": 200, "topK": 40, "topP": 0.95}
    )

    summary_text = response.predictions[0]["content"]

    # Simple heuristic for anomaly detection for demonstration purposes
    anomaly_detected = "anomaly" in summary_text.lower() or "unusual" in summary_text.lower()

    return MetricSummaryResponse(summary=summary_text, anomaly_detected=anomaly_detected)
