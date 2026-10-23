import os
from datetime import datetime, timedelta
from observability_client import get_vertex_ai_model, get_monitoring_client
from google.cloud import monitoring_v3
from google.cloud.aiplatform import telemetry

# Google Cloud project ID and location for Vertex AI
PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
LOCATION = os.environ.get("GCP_LOCATION", "us-central1")

def summarize_metric_trends(
    project_id: str,
    metric_type: str,
    end_time: datetime,
    duration_minutes: int = 60,
    context_info: str = "",
):
    """Summarizes recent metric trends or anomalies using a generative AI model."""
    # First, fetch some raw metric data to provide to the summarization model
    monitoring_client = get_monitoring_client()
    project_name = f"projects/{project_id}"
    start_time = end_time - timedelta(minutes=duration_minutes)
    interval = monitoring_v3.TimeInterval(
        end_time={"seconds": int(end_time.timestamp())},
        start_time={"seconds": int(start_time.timestamp())},
    )
    query_filter = f'metric.type = "{metric_type}"'

    # Fetch a limited number of data points for summarization context
    response = monitoring_client.list_time_series(
        request={
            "name": project_name,
            "filter": query_filter,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.HEADERS, # Only fetch headers for less data
            "page_size": 10,
        }
    )

    metric_data_summary = []
    for ts in response.time_series:
        metric_data_summary.append(
            {
                "metric": ts.metric.type,
                "resource_labels": dict(ts.resource.labels),
            }
        )

    # Prepare prompt for Vertex AI
    prompt = (
        f"Summarize the recent trends and potential anomalies for the metric '{metric_type}' "
        f"over the last {duration_minutes} minutes. "
        f"The metric pertains to project '{project_id}'. "
        f"Here's a brief overview of some time series found: {metric_data_summary}. "
        f"Additional context: {context_info}. "
        "Focus on significant changes, spikes, dips, or sustained patterns." 
        "Use approximately 100-200 words." 
    )

    # Use Vertex AI Generative Model (e.g., gemini-pro)
    model = get_vertex_ai_model(project_id, LOCATION, model_name="gemini-pro")
    
    # Vertex AI uses telemetry for model calls, no direct client import visible
    # but aiplatform.init sets up the context.
    # The concrete model identifier 'gemini-pro' is used here.
    
    responses = model.generate_content(prompt)
    summary_text = responses.text

    return {"metric_type": metric_type, "summary": summary_text}

if __name__ == "__main__":
    # Example usage: Replace with your actual project ID and metric type
    # export GCP_PROJECT_ID="your-gcp-project-id"
    # export GCP_LOCATION="us-central1"
    # trend_summary = summarize_metric_trends(
    #     PROJECT_ID,
    #     "compute.googleapis.com/instance/cpu/utilization",
    #     datetime.utcnow(),
    #     duration_minutes=60,
    #     context_info="This metric is for a critical production service."
    # )
    # print(trend_summary)
    pass
