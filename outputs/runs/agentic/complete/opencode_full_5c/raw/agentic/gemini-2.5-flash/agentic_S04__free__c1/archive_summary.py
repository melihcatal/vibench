import os
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part

def summarize_transcript(project_id: str, location: str, transcript_text: str):
    """Summarizes transcription results using Google Cloud Vertex AI's GenerativeModel.

    Args:
        project_id: The Google Cloud project ID.
        location: The Google Cloud region (e.g., "us-central1").
        transcript_text: The full transcript text to summarize.

    Returns:
        A string containing the summary.
    """
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel("gemini-1.5-pro-preview-0514") # Using a powerful model for summarization

    prompt = f"Summarize the following transcript:

{transcript_text}

Summary:"
    response = model.generate_content(prompt)
    return response.text.strip()

if __name__ == "__main__":
    # Example usage
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = "us-central1" # Or your preferred Vertex AI region
    long_transcript = """
    Good morning, everyone. Welcome to our quarterly earnings call. Today, we'll be discussing our financial performance for the first quarter of 2026.
    I'm pleased to report strong revenue growth across all segments. Our total revenue for Q1 reached $500 million, a 15% increase year-over-year.
    This growth was primarily driven by the success of our new product line, 'InnovateX', which has seen exceptional market adoption.
    Our operating expenses remained well-managed, leading to a healthy profit margin. Net income for the quarter was $75 million, up 20% from the same period last year.
    We also saw significant progress in our strategic initiatives, including the expansion into new international markets and key partnerships that are expected to boost our market share in the coming years.
    Looking ahead, we are optimistic about the rest of the year. We project continued growth, especially with the upcoming launch of 'NextGen Solutions' in Q3.
    We are committed to delivering value to our shareholders and customers.
    Now, I'd like to open the floor for questions.
    """

    if project_id and location:
        print("Generating summary for the transcript...")
        summary = summarize_transcript(project_id, location, long_transcript)
        print("Summary:")
        print(summary)
    else:
        print("GOOGLE_CLOUD_PROJECT or VERTEX_AI_LOCATION environment variable not set.")
