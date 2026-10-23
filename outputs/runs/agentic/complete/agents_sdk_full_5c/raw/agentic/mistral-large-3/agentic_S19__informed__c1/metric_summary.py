from openai import OpenAI
from observability_models import MetricSummaryRequest, MetricSummaryResponse
import json


def metric_summary(request: MetricSummaryRequest) -> MetricSummaryResponse:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Simulated metric data for summarization
    simulated_data = {
        "metric_name": request.metric_name,
        "window_hours": request.window_hours,
        "data_points": [
            {"timestamp": "2023-01-01T00:00:00Z", "value": 42.0},
            {"timestamp": "2023-01-01T12:00:00Z", "value": 45.0},
            {"timestamp": "2023-01-02T00:00:00Z", "value": 120.0}
        ]
    }
    
    prompt = (
        f"Summarize the following metric data for {request.metric_name} over the last {request.window_hours} hours. "
        f"Identify any anomalies or trends. Data: {json.dumps(simulated_data)}. "
        f"Provide the response in {request.locale}."
    )
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    
    summary_text = response.choices[0].message.content
    
    # Simulated anomaly detection
    anomalies = []
    if "120.0" in json.dumps(simulated_data):
        anomalies.append({
            "timestamp": "2023-01-02T00:00:00Z",
            "value": 120.0,
            "reason": "Spike detected"
        })
    
    return MetricSummaryResponse(
        summary_text=summary_text,
        anomalies=anomalies
    )