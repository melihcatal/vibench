import os
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part

def summarize_meeting_transcript_chunk(transcript_chunk: str, project_id: str = None, location: str = "us-central1", model_name: str = "gemini-pro") -> str:
    """Summarizes a chunk of live meeting transcript using Vertex AI's generative models."""
    if project_id is None:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("Google Cloud project ID must be provided or set in GOOGLE_CLOUD_PROJECT env var.")

    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name)

    prompt = f"Summarize the following meeting transcript chunk in a concise manner: '{transcript_chunk}'"

    response = model.generate_content([prompt])

    summary = ""
    if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
        for part in response.candidates[0].content.parts:
            if part.text:
                summary += part.text

    print(f"Summary for chunk '{transcript_chunk[:50]}...': {summary}")
    return summary
