import vertexai
from vertexai.preview.language_models import TextGenerationModel

def metric_summary(payload, config=None):
    config = config or {}
    project_id = config.get("project_id")
    location = config.get("location", "us-central1")
    
    vertexai.init(project=project_id, location=location)
    model = TextGenerationModel.from_pretrained("text-bison@002")

    metric_data = payload["metric_data"]
    # metric_data is expected to be a list of dicts, each with 'timestamp' and 'value'

    # Convert metric data into a more readable format for the LLM
    formatted_data = []
    for point in metric_data:
        formatted_data.append(f"Timestamp: {point['timestamp']}, Value: {point['value']}")
    
    prompt = f"Summarize the following metric data and identify any trends or anomalies: {'; '.join(formatted_data)}"

    response = model.predict(
        prompt,
        temperature=0.2,
        max_output_tokens=1024,
        top_k=40,
        top_p=0.8,
    )
    return {"summary": response.text}
