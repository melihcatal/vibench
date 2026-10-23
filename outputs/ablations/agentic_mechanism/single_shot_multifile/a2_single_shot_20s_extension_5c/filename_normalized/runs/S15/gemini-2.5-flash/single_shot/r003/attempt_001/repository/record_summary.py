import os
import google.cloud.aiplatform as aiplatform

def summarize_document_record(document_text: str, project_id: str = None, location: str = 'us-central1') -> str:
    if project_id is None:
        project_id = os.environ.get('GOOGLE_CLOUD_PROJECT_ID')
    if not project_id:
        raise ValueError("Google Cloud Project ID must be provided or set in GOOGLE_CLOUD_PROJECT_ID environment variable.")

    aiplatform.init(project=project_id, location=location)
    model = aiplatform.GenerativeModel(model_name="gemini-pro")

    prompt = f"Summarize the following document record concisely: {document_text}"
    response = model.generate_content(prompt)
    return response.candidates[0].content.parts[0].text