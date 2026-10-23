from google.cloud import aiplatform
import os


def summarize_analysis_results(analysis_results_text: str) -> str:
    """
    Summarizes visual analysis results using Google Cloud Generative AI (Vertex AI).
    Provider: Google Cloud Vertex AI
    Model: gemini-pro
    """
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    location = os.getenv("GOOGLE_CLOUD_REGION", "us-central1")  # Example region

    aiplatform.init(project=project_id, location=location)

    # Use the gemini-pro model for summarization
    model = aiplatform.preview.generative_models.GenerativeModel("gemini-pro")

    prompt = f"Summarize the following image analysis results concisely: {analysis_results_text}"

    response = model.generate_content(prompt)

    if response.candidates:
        return response.candidates[0].content.parts[0].text
    return "Could not generate a summary."
