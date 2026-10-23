import os
from google.cloud import aiplatform

def summarize_audit_events(events: list[dict]) -> str:
    project_id = os.environ.get("GCP_PROJECT_ID")
    location = os.environ.get("GCP_LOCATION", "us-central1")
    model_name = os.environ.get("GCP_AI_MODEL_NAME", "gemini-pro") # Using gemini-pro as an example

    if not project_id:
        raise ValueError("GCP_PROJECT_ID must be set in environment variables")

    aiplatform.init(project=project_id, location=location)
    
    # Example: Using a simple prompt for summarization
    prompt = f"""Summarize the following federated login audit events:

    {'\n'.join([str(event) for event in events])}

    Provide a concise summary highlighting key activities, potential issues, or trends.
    """

    parameters = {
        "temperature": 0.2,
        "max_output_tokens": 500,
        "top_p": 0.9,
        "top_k": 40,
    }

    model = aiplatform.GenerativeModel(model_name=model_name)
    response = model.generate_content(prompt, generation_config=parameters)
    
    return response.text
