import os
from google.cloud import aiplatform
import vertexai
from vertexai.generative_models import GenerativeModel

PROJECT_ID = os.environ.get("GCP_PROJECT")
LOCATION = os.environ.get("GCP_REGION")


def summarize_meeting_chunk(transcript_chunk: str):
    vertexai.init(project=PROJECT_ID, location=LOCATION)

    model = GenerativeModel("gemini-1.5-flash-001")

    prompt = f"""
    Summarize the following meeting transcript chunk in one sentence:
    
    Transcript:
    "{transcript_chunk}"
    
    Summary:
    """

    response = model.generate_content(prompt)

    return response.text.strip()


if __name__ == "__main__":
    chunk = "Alice said we should probably focus on the user authentication flow first. Bob agreed and mentioned we need to decide on the database schema for users."
    summary = summarize_meeting_chunk(chunk)
    print(f"Chunk: {chunk}")
    print(f"Summary: {summary}")
