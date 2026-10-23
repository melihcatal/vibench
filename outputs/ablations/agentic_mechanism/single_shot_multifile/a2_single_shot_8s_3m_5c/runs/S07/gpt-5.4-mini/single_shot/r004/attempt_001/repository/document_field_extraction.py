from google.cloud import aiplatform_v1
from document_models import first_result_from_analyze


MODEL_ID = "text-bison@002"


def extract_document_fields(normalized_text: str, project_id: str | None = None, location: str = "us-central1") -> dict:
    import os
    project = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project:
        raise ValueError("GOOGLE_CLOUD_PROJECT is required")
    client = aiplatform_v1.PredictionServiceClient()
    endpoint = client.endpoint_path(project=project, location=location, endpoint=MODEL_ID)
    instance = {"content": normalized_text}
    response = client.predict(endpoint=endpoint, instances=[instance])
    text = first_result_from_analyze(response)
    return {"fields": text, "raw": response}
