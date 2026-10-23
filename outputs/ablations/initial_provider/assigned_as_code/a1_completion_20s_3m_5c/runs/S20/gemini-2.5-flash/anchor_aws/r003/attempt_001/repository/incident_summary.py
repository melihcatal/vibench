import os
from typing import List, Dict, Any
from google.cloud import aiplatform

from observability_models import IncidentSummaryRequest

def summarize_incident(request: IncidentSummaryRequest, project_id: str, location: str = "us-central1") -> str:
    aiplatform.init(project=project_id, location=location)
    
    # Use the specific model identifier for a text generation model
    # For example, using 'gemini-pro' which is a common choice for text generation
    model_id = os.environ.get("VERTEX_AI_GENERATIVE_MODEL_ID", "gemini-pro")
    model = aiplatform.preview.language_models.ChatModel.from_pretrained(model_id)

    # Prepare the prompt for summarization
    log_entries_text = "\n".join([str(log) for log in request.error_logs])
    prompt = f"Summarize the following error logs to provide a concise incident overview. Highlight key issues, potential causes, and affected components:\n\n{log_entries_text}\n\nIncident Summary:"
    
    # Generate the summary
    response = model.predict(prompt=prompt)
    return response.text
