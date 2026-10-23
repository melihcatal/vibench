
import os
from google.cloud import aiplatform

def summarize_transcript_chunk(transcript_chunk: str) -> str:
    """
    Summarizes a given chunk of meeting transcript using Google's Generative AI.

    Args:
        transcript_chunk: A string containing a portion of the meeting transcript.

    Returns:
        A string containing the summary of the transcript chunk.
    """
    # Initialize Google Cloud AI Platform (Vertex AI)
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or
    # authenticate using `gcloud auth application-default login`
    # Replace 'your-project-id' and 'your-location' with your GCP project ID and region
    project_id = os.getenv("GCP_PROJECT_ID", "your-project-id")
    location = os.getenv("GCP_LOCATION", "us-central1")
    aiplatform.init(project=project_id, location=location)

    # Use the 'gemini-pro' model for summarization
    model = aiplatform.GenerativeModel("gemini-pro")

    prompt = f"""
    Please summarize the following meeting transcript chunk concisely:

    "{transcript_chunk}"
    """

    response = model.generate_content(prompt)
    return response.text.strip()

if __name__ == "__main__":
    # Example Usage:
    sample_transcript = """
    "Good morning everyone. Today we're going to discuss the Q3 financial results. Sarah, could you start with the revenue figures?"
    "Certainly. For Q3, our total revenue reached $150 million, which is a 10% increase from the previous quarter. The primary drivers for this growth were our new product line and expanded market reach in Asia."
    "That's excellent news, Sarah. Mark, what about the profit margins?"
    "Our gross profit margin stood at 45%, a slight improvement from Q2. However, operational expenses increased due to marketing campaigns for the new product launch, bringing our net profit margin to 18%."
    """
    summary = summarize_transcript_chunk(sample_transcript)
    print("Summary of the transcript chunk:")
    print(summary)
