import os
from typing import Dict, Any
from google.cloud import aiplatform

def check_text_safety(project_id: str, location: str, text_content: str) -> Dict[str, Any]:
    """
    Checks user-generated document fields for unsafe content using Google Cloud Vertex AI's gemini-pro model.

    Args:
        project_id: The Google Cloud project ID.
        location: The Google Cloud region (e.g., "us-central1").
        text_content: The text content to check for safety.

    Returns:
        A dictionary containing the safety attributes and scores.
    """
    aiplatform.init(project=project_id, location=location)
    # Using the gemini-pro model for safety attribute checking
    # https://cloud.google.com/vertex-ai/docs/generative/safety-filters
    model = aiplatform.GenerativeModel("gemini-pro")

    response = model.generate_content(
        contents=text_content,
        safety_settings=[
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]
    )

    # The safety attributes are usually in the 'prompt_feedback' or 'candidates' part of the response
    safety_attributes = {}
    if response.prompt_feedback:
        for safety_rating in response.prompt_feedback.safety_ratings:
            safety_attributes[safety_rating.category.name] = {
                "score": safety_rating.score.name,
                "blocked": safety_rating.blocked
            }
    # If the content was blocked, this will be in the response.candidates[0].finish_reason or other fields
    # For this simplified example, we'll just return what's directly available from prompt_feedback
    return safety_attributes
