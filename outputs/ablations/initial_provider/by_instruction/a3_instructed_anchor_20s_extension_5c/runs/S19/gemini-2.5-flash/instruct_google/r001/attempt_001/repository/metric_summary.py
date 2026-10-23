from google.cloud import aiplatform
from observability_models import MetricQueryResult

def summarize_metric_trends(project_id: str, location: str, metric_data: MetricQueryResult) -> str:
    aiplatform.init(project=project_id, location=location)
    
    # Using a text-bison model for summarization. Adjust model name if needed.
    model = aiplatform.PreviewModel.from_pretrained("text-bison")

    # Prepare the prompt for summarization
    metric_values = ", ".join([f"({dp.timestamp}, {dp.value})" for dp in metric_data.datapoints])
    prompt = f"Summarize the trends and any anomalies observed in the metric ''{metric_data.metric_name}'' with the following data points (timestamp, value): {metric_values}"

    response = model.predict([prompt])
    
    if response.predictions:
        # Accessing the first prediction, assuming it's a string
        return response.predictions[0].strip()
    return "No summary available."
