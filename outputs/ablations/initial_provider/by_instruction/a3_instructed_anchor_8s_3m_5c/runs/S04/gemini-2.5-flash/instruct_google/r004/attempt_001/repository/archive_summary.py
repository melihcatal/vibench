import os
from typing import List
from speech_models import TranscriptionResult
from vertexai.preview.generative_models import GenerativeModel, Part, Image
import vertexai

def archive_summary(transcript_result: TranscriptionResult) -> str:
    """Summarize transcription results using Google Cloud Generative AI (Vertex AI).

    Args:
        transcript_result: The TranscriptionResult object containing the transcript to summarize.

    Returns:
        A string containing the summary of the transcript.
    """
    # Initialize Vertex AI
    project_id = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id")  # Replace with your GCP project ID
    location = os.environ.get("GCP_REGION", "us-central1") # Replace with your GCP region
    vertexai.init(project=project_id, location=location)

    model = GenerativeModel("gemini-pro") # Using gemini-pro model for summarization

    full_transcript = " ".join([alt.transcript for alt in transcript_result.alternatives])
    
    if not full_transcript:
        return ""

    prompt = f"Summarize the following meeting transcript: {full_transcript}"

    response = model.generate_content([prompt])
    
    return response.text
