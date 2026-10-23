import os
from google.cloud import aiplatform

def summarize_message(text: str, project_id: str = None, region: str = None) -> str:
    if not project_id:
        project_id = os.environ.get("GCP_PROJECT_ID")
    if not region:
        region = os.environ.get("GCP_REGION", "us-central1")

    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable or argument not set.")

    aiplatform.init(project=project_id, location=region)

    parameters = {
        "temperature": 0.2,
        "max_output_tokens": 256,
        "top_p": 0.95,
        "top_k": 40
    }

    model = aiplatform.preview.language_models.TextGenerationModel.from_pretrained("gemini-pro")

    prompt = f"Summarize the following text in a concise manner:\n\n{text}"

    response = model.predict(prompt, **parameters)

    return response.text.strip()
