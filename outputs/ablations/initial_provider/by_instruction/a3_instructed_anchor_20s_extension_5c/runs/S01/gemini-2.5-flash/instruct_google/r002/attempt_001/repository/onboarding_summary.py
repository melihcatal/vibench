import os
from google.cloud import aiplatform

def onboarding_summary(onboarding_state_text):
    """
    Summarizes onboarding state for support using Google Cloud Vertex AI (generative model).
    Requires GOOGLE_APPLICATION_CREDENTIALS and PROJECT_ID to be set in the environment.
    """
    project_id = os.environ.get("PROJECT_ID")
    if not project_id:
        raise ValueError("PROJECT_ID environment variable not set.")

    # Initialize Vertex AI SDK
    aiplatform.init(project=project_id, location="us-central1") # Use an appropriate region

    # Use the Gemini Pro model for summarization.
    # The model identifier 'gemini-pro' makes the provider identifiable.
    model = aiplatform.preview.generative_models.GenerativeModel("gemini-pro")

    prompt = f"Summarize the following user onboarding state for a support agent:\n\n{onboarding_state_text}"

    response = model.generate_content(prompt)

    return response.text
