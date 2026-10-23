import os
from typing import Dict
from google.cloud import aiplatform

# Provider-specific model identifier
TEXT_MODERATION_MODEL_ID = "text-moderation@001"


def check_text_safety(
    text: str, project_id: str, location: str = "us-central1"
) -> Dict:
    """
    Checks text for unsafe content using the Google Cloud Vertex AI Text Moderation API.

    Args:
        text: The text to check.
        project_id: Your Google Cloud project ID.
        location: The GCP location for the Vertex AI endpoint.

    Returns:
        A dictionary containing the moderation results.
    """
    aiplatform.init(project=project_id, location=location)

    # Provider-specific model loading
    model = aiplatform.from_pretrained(TEXT_MODERATION_MODEL_ID)

    response = model.predict([text])

    # The response object is a list of predictions, one for each input text.
    prediction = response.predictions[0]

    return dict(prediction)
