
import os
from google.cloud import aiplatform

def summarize_transcription(transcription_text: str) -> str:
    """
    Summarizes transcription results using Google Cloud's Vertex AI.

    Args:
        transcription_text: The full text of the transcription.

    Returns:
        A summarized version of the transcription.
    """
    # Initialize Vertex AI
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    aiplatform.init(project=project_id, location="us-central1")

    # Load the Gemini Pro model
    model = aiplatform.preview.language_models.TextGenerationModel.from_pretrained("gemini-pro")

    # Craft the prompt for summarization
    prompt = f"Summarize the following meeting transcript:

{transcription_text}"

    # Generate the summary
    response = model.predict(prompt=prompt)

    return response.text

