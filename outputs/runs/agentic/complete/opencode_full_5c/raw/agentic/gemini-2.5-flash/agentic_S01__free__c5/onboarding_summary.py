from google.cloud import aiplatform
from vertexai.preview.generative_models import GenerativeModel  # For gemini-pro
from identity_models import UserProfile, OnboardingSummary
import os


def onboarding_summary(user_profile: UserProfile) -> OnboardingSummary:
    # Initialize Vertex AI
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")  # Ensure this env var is set
    location = os.environ.get(
        "GOOGLE_CLOUD_LOCATION", "us-central1"
    )  # e.g., us-central1

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    aiplatform.init(project=project_id, location=location)

    # Using a generative model like gemini-pro for summarization
    # Ensure gemini-pro is available in your specified location.
    model = GenerativeModel("gemini-pro")  # Model ID for Vertex AI's Gemini Pro

    prompt = f"Summarize the following user onboarding profile for support purposes:\n"
    prompt += f"User ID: {user_profile.uid}\n"
    prompt += f"Display Name: {user_profile.display_name}\n"
    prompt += f"Bio: {user_profile.bio}\n"
    prompt += f"Locale: {user_profile.locale}\n"
    prompt += f"Summary:"

    response = model.generate_content(prompt)
    summary_text = response.text.strip()

    return OnboardingSummary(user_id=user_profile.uid, summary_text=summary_text)
