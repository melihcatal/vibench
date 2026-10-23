import json

from google.cloud import aiplatform

def summarize_metric_trends(metric_data: dict, config=None):
    config = config or {}
    # Initialize Vertex AI
    aiplatform.init(project=config["project_id"], location=config.get("region", "us-central1"))

    # Use the Gemini Pro model
    model = aiplatform.preview.generative_models.GenerativeModel("gemini-pro")

    # Prepare the prompt for summarization
    prompt = f"Summarize the following metric data, identifying any trends or anomalies: {json.dumps(metric_data)}"

    # Generate content using the model
    response = model.generate_content(prompt)

    return {"summary": response.text}
