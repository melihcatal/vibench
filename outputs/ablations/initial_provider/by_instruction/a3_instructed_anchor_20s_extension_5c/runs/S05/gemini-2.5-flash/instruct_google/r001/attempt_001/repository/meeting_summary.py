import os
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part, Image

def summarize_meeting_transcript(
    transcript_chunks: list[str],
    project_id: str = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id"),
    location: str = "us-central1"
) -> str:
    """Summarizes live meeting transcript chunks using Google's Generative AI (Vertex AI)."""

    vertexai.init(project=project_id, location=location)
    model = GenerativeModel("gemini-pro") # Using gemini-pro for text summarization

    full_transcript = "\n".join(transcript_chunks)

    prompt = f"""Summarize the following meeting transcript:

{full_transcript}

Summary:"""

    response = model.generate_content(prompt)
    return response.text
