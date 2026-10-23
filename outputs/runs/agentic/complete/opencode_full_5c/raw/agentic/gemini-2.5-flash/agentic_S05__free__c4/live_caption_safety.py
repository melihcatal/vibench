import os

from google.cloud import aiplatform
from vertexai.preview.generative_models import (
    GenerativeModel,
    HarmCategory,
    HarmBlockThreshold,
)


def check_content_safety(text: str) -> dict:
    """Checks live transcript text for unsafe content using Google Cloud Vertex AI generative models."""
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print(
            "Warning: GOOGLE_APPLICATION_CREDENTIALS environment variable not set for Vertex AI."
        )

    # Initialize Vertex AI
    # Replace 'your-project-id' and 'your-location' with your actual project ID and desired location
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "your-project-id")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    aiplatform.init(project=project_id, location=location)

    model = GenerativeModel("gemini-pro")  # Using gemini-pro for content moderation

    # Configure safety settings
    safety_settings = {
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    }

    try:
        response = model.generate_content([text], safety_settings=safety_settings)
        # If the response is blocked due to safety, response.candidates will be empty
        if not response.candidates:
            return {"safe": False, "reason": "Content blocked by safety settings"}
        else:
            # If content is not blocked, it's considered safe for this check.
            # More granular safety analysis might involve checking response.prompt_feedback.safety_ratings
            # if detailed category-wise feedback is needed.
            return {"safe": True, "reason": "Content passed safety checks"}

    except Exception as e:
        # Catching potential errors during content generation, e.g., API issues or input errors.
        return {"safe": False, "reason": f"Error during safety check: {str(e)}"}
