import vertexai
from vertexai.generative_models import GenerativeModel, Part
import os

class OnboardingSummaryRequest:
    def __init__(self, onboarding_data: str):
        self.onboarding_data = onboarding_data

class OnboardingSummaryResponse:
    def __init__(self, summary: str):
        self.summary = summary

def onboarding_summary(request: OnboardingSummaryRequest) -> OnboardingSummaryResponse:
    # Initialize Vertex AI
    # Ensure GOOGLE_APPLICATION_CREDENTIALS and GOOGLE_CLOUD_PROJECT environment variables are set
    # Or explicitly pass project and location to vertexai.init()
    try:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")
        
        vertexai.init(project=project_id, location="us-central1") # Or your preferred region
    except Exception as e:
        print(f"Error initializing Vertex AI: {e}")
        raise

    model = GenerativeModel("gemini-pro") # Using gemini-pro for text generation

    prompt = f"Summarize the following user onboarding data for support personnel. Highlight any incomplete sections or potential issues:\n\n{request.onboarding_data}"

    try:
        response = model.generate_content([prompt])
        return OnboardingSummaryResponse(summary=response.text)
    except Exception as e:
        print(f"Error summarizing onboarding data: {e}")
        raise
