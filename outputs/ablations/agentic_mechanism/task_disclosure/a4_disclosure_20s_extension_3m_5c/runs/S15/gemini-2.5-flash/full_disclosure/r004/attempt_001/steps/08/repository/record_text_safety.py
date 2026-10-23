from google.cloud import aiplatform
from vertexai.preview.generative_models import GenerativeModel, Part

def check_unsafe_content(text_content: str) -> dict:
    """
    Checks user-generated document fields for unsafe content using Google Cloud Vertex AI's gemini-pro model.

    Args:
        text_content: The text content to check for unsafe material.

    Returns:
        A dictionary indicating if the content is unsafe and providing safety attributes.
    """
    # Initialize Vertex AI
    aiplatform.init()

    # Load the Gemini Pro model
    model = GenerativeModel("gemini-pro")

    # Generate content with safety settings
    response = model.generate_content(
        [Part.from_text(text_content)],
        safety_settings={
            "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
            "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
            "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
            "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
        },
    )

    # Check for safety attributes
    is_unsafe = False
    safety_ratings = []

    if response.prompt_feedback and response.prompt_feedback.safety_ratings:
        for rating in response.prompt_feedback.safety_ratings:
            safety_ratings.append({
                "category": rating.category.name,
                "probability": rating.probability.name,
                "blocked": rating.blocked
            })
            if rating.blocked:
                is_unsafe = True

    return {
        "is_unsafe": is_unsafe,
        "safety_ratings": safety_ratings,
        "provider": "Google Cloud Vertex AI",
        "model_id": "gemini-pro"
    }
