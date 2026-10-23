import os
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part

def summarize_transcript(transcript: str, project_id: str, location: str = "us-central1"):
    """Summarizes transcription results using Google Cloud Vertex AI's Generative AI.

    Args:
        transcript: The full transcript text to summarize.
        project_id: Your Google Cloud project ID.
        location: The Google Cloud region for Vertex AI.

    Returns:
        The summarized text.
    """
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel("gemini-pro") # Using gemini-pro for summarization
    
    prompt = f"Please summarize the following transcript:

{transcript}

Summary:"

    response = model.generate_content([prompt])
    summary = response.candidates[0].content.parts[0].text

    print(f"Generated summary: {summary}")
    return summary
