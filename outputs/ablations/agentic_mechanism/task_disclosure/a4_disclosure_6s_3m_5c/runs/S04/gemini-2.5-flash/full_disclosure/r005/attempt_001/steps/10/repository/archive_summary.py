import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part
import os

def summarize_transcript(transcript_text: str) -> str:
    """
    Summarizes transcription results using Google's Gemini Pro model.

    Args:
        transcript_text: The full text of the transcript to summarize.

    Returns:
        A summarized version of the transcript.
    """
    # Initialize Vertex AI
    vertexai.init(project=os.environ.get("GOOGLE_CLOUD_PROJECT"), location=os.environ.get("GOOGLE_CLOUD_REGION"))

    # Load the Gemini Pro model
    model = GenerativeModel("gemini-pro")

    # Define the prompt for summarization
    prompt = f"Please summarize the following meeting transcript:

{transcript_text}

Summary:"

    # Generate content
    response = model.generate_content(prompt)

    return response.text

