import os
from google.cloud import aiplatform
import vertexai
from vertexai.generative_models import GenerativeModel, HarmCategory, HarmBlockThreshold

def check_unsafe_content(log_message: str) -> dict:
    """
    Checks selected log message text for unsafe content using Google Cloud Vertex AI.

    Args:
        log_message: The log message text to check.

    Returns:
        A dictionary containing the safety assessment.
    """
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    vertexai.init(project=project_id, location=location)
    model = GenerativeModel("gemini-pro")

    response = model.generate_content(
        [log_message],
        safety_settings={
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        },
    )

    safety_ratings = []
    if hasattr(response, 'candidates') and response.candidates:
        for candidate in response.candidates:
            if hasattr(candidate, 'safety_ratings'):
                for rating in candidate.safety_ratings:
                    safety_ratings.append({
                        "category": rating.category.name,
                        "probability": rating.probability.name,
                        "blocked": rating.blocked
                    })
    
    return {"safety_ratings": safety_ratings}

