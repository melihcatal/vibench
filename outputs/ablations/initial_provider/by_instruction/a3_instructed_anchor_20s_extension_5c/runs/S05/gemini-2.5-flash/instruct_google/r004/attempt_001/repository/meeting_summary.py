import vertexai
from vertexai.generative_models import GenerativeModel, Part

def summarize_meeting_chunks(transcript_chunks: list[str]) -> str:
    vertexai.init(project="YOUR_PROJECT_ID", location="YOUR_REGION") # Replace with your project ID and region
    model = GenerativeModel("gemini-pro")

    full_transcript = " ".join(transcript_chunks)

    prompt = f"Summarize the following meeting transcript:\n\n{full_transcript}\n\nSummary:"

    response = model.generate_content(prompt)

    return response.text
