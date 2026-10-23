import os
from observability_client import ObservabilityClient
from observability_models import IncidentSummaryRequest, IncidentSummaryResponse
from vertexai.preview.language_models import TextGenerationModel

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
if not PROJECT_ID:
    raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set")

LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1") # Default to us-central1

def incident_summary(request: IncidentSummaryRequest) -> IncidentSummaryResponse:
    client = ObservabilityClient(project_id=PROJECT_ID)
    model = client.get_text_generation_model()

    log_text = "\n".join(request.log_entries)
    prompt = f"""Summarize the following error logs for an incident review. Identify key errors, potential causes, and affected areas:

{log_text}

Summary:"""

    response = model.predict(
        prompt,
        temperature=0.2,
        max_output_tokens=1024,
        top_p=0.9,
        top_k=40
    )

    return IncidentSummaryResponse(summary=response.text)
