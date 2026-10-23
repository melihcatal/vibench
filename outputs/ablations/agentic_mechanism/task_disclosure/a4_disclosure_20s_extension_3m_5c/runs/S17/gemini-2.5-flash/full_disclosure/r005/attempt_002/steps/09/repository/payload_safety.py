import os
from google.cloud import aiplatform
from vertexai.preview.generative_models import GenerativeModel, Part

def check_payload_safety(payload: str) -> dict:
    """
    Checks the decrypted text payload for unsafe content using Google's Vertex AI.

    Args:
        payload: The decrypted text payload to check.

    Returns:
        A dictionary containing the safety status and any safety ratings.
    """
    # Initialize Vertex AI
    aiplatform.init(project=os.getenv("GOOGLE_CLOUD_PROJECT"), location=os.getenv("GOOGLE_CLOUD_REGION"))

    # Load the model
    model = GenerativeModel("gemini-1.5-flash")

    # Generate content with safety settings
    response = model.generate_content(
        [Part.from_text(payload)],
        safety_settings={
            "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
            "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
            "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
            "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
        }
    )

    safety_attributes = {}
    is_safe = True

    if hasattr(response, 'prompt_feedback') and response.prompt_feedback:
        for rating in response.prompt_feedback.safety_ratings:
            safety_attributes[rating.category.name] = rating.probability.name
            if rating.blocked:
                is_safe = False

    return {"is_safe": is_safe, "safety_attributes": safety_attributes}
