import os
from google.cloud import aiplatform

def embedding_job_summary(payload: dict, config: dict = None) -> dict:
    config = config or {}
    project = config.get("google_cloud_project") or os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = config.get("google_cloud_location") or os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

    if not project:
        raise ValueError("Google Cloud project not provided or found in environment variables.")

    aiplatform.init(project=project, location=location)

    # Using a specific model for text generation
    model_name = config.get("summary_model") or "gemini-pro"
    model = aiplatform.TextGenerationModel.from_pretrained(model_name)

    embedding_results = payload.get("embedding_results", [])
    summary_prompt = f"Summarize the following embedding job results:\n\n{embedding_results}"

    response = model.predict(summary_prompt)
    return {"summary": response.text}
