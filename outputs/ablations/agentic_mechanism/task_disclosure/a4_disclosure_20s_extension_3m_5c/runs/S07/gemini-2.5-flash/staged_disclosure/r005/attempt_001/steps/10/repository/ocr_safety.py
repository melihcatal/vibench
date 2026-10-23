import os
from google.cloud import aiplatform
from google.generativeai.types import HarmCategory, HarmBlockThreshold

def check_unsafe_content(document_text: str) -> dict:
    """
    Checks extracted document text for unsafe content using Google Cloud Vertex AI's gemini-pro model.

    Args:
        document_text: The text extracted from a document.

    Returns:
        A dictionary indicating if the content is safe and any safety ratings.
    """
    try:
        # Initialize Vertex AI
        aiplatform.init(project=os.environ.get("GOOGLE_CLOUD_PROJECT"), location=os.environ.get("GOOGLE_CLOUD_REGION", "us-central1"))

        # Load the generative model
        model = aiplatform.preview.language_models.ChatModel.from_pretrained("gemini-pro")

        # The safety settings are typically handled by the model itself or can be explicitly set
        # For this example, we'll rely on the default safety settings of gemini-pro
        # and simply send the text for content generation/analysis.
        # The response will contain safety attributes if any issues are detected.

        response = model.send_message(document_text)

        safety_ratings = response.prompt_feedback.safety_ratings
        
        unsafe_categories = []
        for rating in safety_ratings:
            if rating.blocked:
                unsafe_categories.append(rating.category.name)

        if unsafe_categories:
            return {
                "is_safe": False,
                "unsafe_categories": unsafe_categories,
                "full_safety_ratings": [
                    {"category": r.category.name, "probability": r.probability.name, "blocked": r.blocked}
                    for r in safety_ratings
                ]
            }
        else:
            return {
                "is_safe": True,
                "full_safety_ratings": [
                    {"category": r.category.name, "probability": r.probability.name, "blocked": r.blocked}
                    for r in safety_ratings
                ]
            }

    except Exception as e:
        return {"error": str(e)}

