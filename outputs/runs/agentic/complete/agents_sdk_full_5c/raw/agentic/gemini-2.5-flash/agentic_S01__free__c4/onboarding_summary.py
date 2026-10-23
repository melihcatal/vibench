import os
from google.cloud import aiplatform

# Google Cloud Project ID and Location for Vertex AI
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1") # Default to us-central1

# Model ID for summarization, typically a large language model like `text-bison` or `gemini-pro`.
MODEL_ID = "gemini-pro" # Using gemini-pro for summarization

def summarize_onboarding_state(onboarding_data: str) -> str:
    """Summarizes the onboarding state using Google Cloud Vertex AI generative model."""
    if not PROJECT_ID:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    aiplatform.init(project=PROJECT_ID, location=LOCATION)
    model = aiplatform.GenerativeModel(MODEL_ID)

    prompt = f"""Summarize the following onboarding state information concisely for a support agent.
    
    Onboarding Data: """
    {onboarding_data}
    """
    """

    try:
        response = model.generate_content(prompt)
        # Assuming the model's response for summarization is directly usable.
        summary = response.candidates[0].content.parts[0].text.strip()
        return summary
    except Exception as e:
        raise RuntimeError(f"Failed to summarize onboarding state using Vertex AI: {e}")
