import os
import vertexai
from vertexai.generative_models import GenerativeModel, Part

def meeting_summary(transcript_chunks: list[str], project_id: str, location: str = "us-central1"):
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel("gemini-pro")

    full_transcript = " ".join(transcript_chunks)

    prompt = f"Summarize the following meeting transcript:\n\n{full_transcript}\n\nSummary:"

    response = model.generate_content(prompt)

    return response.text
