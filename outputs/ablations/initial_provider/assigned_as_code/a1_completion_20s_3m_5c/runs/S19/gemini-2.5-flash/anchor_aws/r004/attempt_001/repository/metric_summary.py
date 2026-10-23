import vertexai
from vertexai.preview.language_models import TextGenerationModel

def metric_summary(payload, config=None):
    config = config or {}
    
    vertexai.init(project=config["gcp_project_id"], location=config.get("gcp_location", "us-central1"))
    model = TextGenerationModel.from_pretrained("text-bison-32k") # Using a suitable model for summarization

    # The payload is expected to contain a 'metric_data' field with string representation of metric trends/anomalies
    # This could be a collection of data points, or pre-analyzed text about trends
    prompt = f"Summarize the following metric data and identify any significant trends or anomalies:\n\n{payload['metric_data']}"

    response = model.predict(prompt=prompt, temperature=0.2, max_output_tokens=1024)
    return {"summary": response.text}
