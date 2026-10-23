import vertexai
from vertexai.generative_models import GenerativeModel, HarmCategory, HarmBlockThreshold
import os


def check_content_safety(
    text: str, project_id: str, location: str = "us-central1"
) -> dict:
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel("gemini-pro")
    response = model.generate_content(
        text,
        safety_settings={
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HAR_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HAR_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        },
    )
    if response._error:
        return {"error": response._error}
    return {"safety_ratings": response.prompt_feedback.safety_ratings}
