from google.cloud import aiplatform
import os

def summarize_record(text_content, project_id=None, location=None):
    project_id = project_id or os.environ.get("GCP_PROJECT_ID")
    location = location or os.environ.get("GCP_LOCATION", "us-central1")

    if not project_id:
        raise ValueError("Google Cloud project ID must be provided or set in GCP_PROJECT_ID environment variable.")

    aiplatform.init(project=project_id, location=location)

    # Using a generative model for summarization, e.g., gemini-pro
    # Note: Ensure the model is available in the specified location.
    try:
        model = aiplatform.GenerativeModel("gemini-pro")
        response = model.generate_content(f"Summarize the following text: {text_content}")
        return response.text
    except Exception as e:
        # Fallback to text-bison if gemini-pro is not available or for different use cases
        model = aiplatform.TextGenerationModel.from_pretrained("text-bison@001")
        response = model.predict(f"Summarize the following text: {text_content}")
        return response.text
