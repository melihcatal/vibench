import os
from vertexai.preview.generative_models import GenerativeModel, Part
import vertexai


def summarize_onboarding_state(
    onboarding_data: str, project_id: str | None = None, location: str = "us-central1"
) -> str:
    # Initialize Vertex AI
    vertexai.init(
        project=project_id or os.getenv("GOOGLE_CLOUD_PROJECT"), location=location
    )

    # Use the Gemini Pro model for summarization
    model = GenerativeModel("gemini-pro")  # Concrete model identifier

    prompt = f"Summarize the following user onboarding information in a concise manner for support personnel:\n\n{onboarding_data}\n\nSummary:"

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise RuntimeError(
            f"Failed to summarize onboarding state using Gemini Pro: {e}"
        )
