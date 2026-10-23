import os
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part

def check_unsafe_content(text_payload: str) -> dict:
    """
    Checks the given text payload for unsafe content using Google Vertex AI.

    Args:
        text_payload: The text content of the message payload to check.

    Returns:
        A dictionary containing the safety analysis result.
    """
    # Initialize Vertex AI with your project and location
    # Replace 'your-project-id' and 'your-location' with your actual GCP project ID and region.
    # It's recommended to set these as environment variables or fetch from a configuration service.
    project_id = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id")
    location = os.environ.get("GCP_LOCATION", "us-central1") # Example region

    vertexai.init(project=project_id, location=location)

    model = GenerativeModel("gemini-pro")
    
    # You can configure safety settings for the model if needed
    # For demonstration, we'll rely on default safety filters.
    
    response = model.generate_content(
        [Part.from_text(text_payload)],
        safety_settings={
            "HARM_CATEGORY_HARASSMENT": "BLOCK_MEDIUM_AND_ABOVE",
            "HARM_CATEGORY_HATE_SPEECH": "BLOCK_MEDIUM_AND_ABOVE",
            "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_MEDIUM_AND_ABOVE",
            "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_MEDIUM_AND_ABOVE",
        }
    )

    safety_ratings = []
    if hasattr(response, 'prompt_feedback') and hasattr(response.prompt_feedback, 'safety_ratings'):
        for rating in response.prompt_feedback.safety_ratings:
            safety_ratings.append({
                "category": rating.category.name,
                "probability": rating.probability.name,
                "is_blocked": rating.is_blocked
            })
    
    # Determine if the content is safe based on prompt feedback
    is_safe = True
    if hasattr(response, 'prompt_feedback') and response.prompt_feedback.block_reason:
        is_safe = False

    return {
        "is_safe": is_safe,
        "safety_ratings": safety_ratings,
        "raw_response": str(response) # Include raw response for detailed inspection if needed
    }

