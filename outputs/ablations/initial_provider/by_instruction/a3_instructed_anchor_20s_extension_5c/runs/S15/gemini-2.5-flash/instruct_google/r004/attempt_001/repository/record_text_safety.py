import vertexai
from vertexai.preview.generative_models import GenerativeModel, HarmCategory, HarmBlockThreshold
import os

def record_text_safety(text_content: str) -> dict:
    """Checks user-generated document fields for unsafe content using Google Cloud Generative AI.

    Args:
        text_content (str): The text content to check for safety.

    Returns:
        dict: A dictionary containing safety attributes and scores.
    """
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_REGION", "us-central1") # Default to us-central1

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    vertexai.init(project=project_id, location=location)
    model = GenerativeModel("gemini-pro")

    if not text_content:
        return {"safety_status": "No content to check.", "scores": {}}

    response = model.generate_content(
        text_content,
        safety_settings={
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.HARM_BLOCK_THRESHOLD_UNSPECIFIED,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.HARM_BLOCK_THRESHOLD_UNSPECIFIED,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.HARM_BLOCK_THRESHOLD_UNSPECIFIED,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.HARM_BLOCK_THRESHOLD_UNSPECIFIED,
        },
    )

    safety_attributes = {"safety_status": "Safe", "scores": {}}
    if response._candidate_data and response._candidate_data[0].safety_ratings:
        for rating in response._candidate_data[0].safety_ratings:
            category = str(rating.category).split('.')[-1]
            threshold = str(rating.probability).split('.')[-1]
            safety_attributes["scores"][category] = threshold
            if rating.blocked: # if any category is blocked
                safety_attributes["safety_status"] = "Unsafe"

    print("Text content safety check completed using Google Cloud Generative AI.")
    return safety_attributes
