from google.cloud import aiplatform
from vertexai.preview.generative_models import GenerativeModel, HarmCategory, Part, Tool, Image

def check_text_safety(text: str) -> dict:
    """
    Checks user-generated document fields for unsafe content using Google Cloud Vertex AI.

    Args:
        text: The text content to check for safety.

    Returns:
        A dictionary containing the safety analysis results.
    """
    model = GenerativeModel("gemini-pro")
    response = model.generate_content(
        [text],
        safety_settings={
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmCategory.HARM_CATEGORY_UNSPECIFIED,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmCategory.HARM_CATEGORY_UNSPECIFIED,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmCategory.HARM_CATEGORY_UNSPECIFIED,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmCategory.HARM_CATEGORY_UNSPECIFIED,
        },
    )

    safety_ratings = {}
    if hasattr(response, 'prompt_feedback') and hasattr(response.prompt_feedback, 'safety_ratings'):
        for rating in response.prompt_feedback.safety_ratings:
            safety_ratings[rating.category.name] = rating.probability.name
    
    return {"safety_ratings": safety_ratings}
