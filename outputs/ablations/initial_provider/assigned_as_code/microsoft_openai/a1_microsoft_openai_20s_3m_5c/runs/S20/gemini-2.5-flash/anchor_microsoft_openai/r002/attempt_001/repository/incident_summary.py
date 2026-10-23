from observability_models import LogEntry, IncidentSummaryRequest
from google.cloud import aiplatform
import os

def incident_summary(request: IncidentSummaryRequest, project_id: str = None, location: str = "us-central1"):
    project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("Google Cloud Project ID not provided and GOOGLE_CLOUD_PROJECT environment variable not set.")

    aiplatform.init(project=project_id, location=location)
    
    # Using a text-bison model for summarization, which is part of Vertex AI Generative AI offerings.
    # For more advanced scenarios, a fine-tuned model or a different generative model might be used.
    from vertexai.preview.language_models import TextGenerationModel
    model = TextGenerationModel.from_pretrained("text-bison")

    log_messages = [f"Severity: {entry.severity}, Timestamp: {entry.timestamp}, Resource: {entry.resource_type}/{entry.resource_id}, Message: {entry.message}" for entry in request.log_entries]
    full_log_text = "\n".join(log_messages)

    prompt = f"""Summarize the following log entries for an incident review. Focus on identifying key issues, potential causes, and affected components.
    
    Log Entries:
    {full_log_text}
    
    Summary Type: {request.summary_type}
    
    Incident Summary:"""

    response = model.predict(prompt=prompt, temperature=0.2, max_output_tokens=1024)
    
    return {"summary": response.text}
