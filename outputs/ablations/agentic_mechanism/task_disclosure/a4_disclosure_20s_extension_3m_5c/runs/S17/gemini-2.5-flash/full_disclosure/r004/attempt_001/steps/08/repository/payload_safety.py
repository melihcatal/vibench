import os
import vertexai
from vertexai.preview.generative_models import GenerativeModel

def check_payload_safety(text_payload: str) -> dict:
    """
    Checks decrypted text payloads for unsafe content using Google Cloud Vertex AI.

    Args:
        text_payload: The decrypted text content to check.

    Returns:
        A dictionary containing the safety attributes of the text.
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    vertexai.init(project=project_id, location="us-central1")

    model = GenerativeModel("gemini-pro")

    response = model.generate_content(
        [text_payload]
    )

    safety_attributes = {}
    if response.prompt_feedback and response.prompt_feedback.safety_ratings:
        safety_attributes["prompt_safety_ratings"] = [
            {"category": rating.category.name, "probability": rating.probability.name}
            for rating in response.prompt_feedback.safety_ratings
        ]

    return safety_attributes
