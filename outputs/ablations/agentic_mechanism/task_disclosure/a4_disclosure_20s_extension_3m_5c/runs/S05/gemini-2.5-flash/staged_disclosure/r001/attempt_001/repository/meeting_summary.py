import google.generativeai as genai
import os

def summarize_transcript_chunk(transcript_chunk: str) -> str:
    """
    Summarizes a single chunk of a live meeting transcript using Google's Generative AI.

    Args:
        transcript_chunk: A string representing a chunk of the meeting transcript.

    Returns:
        A string containing the summary of the transcript chunk.
    """
    # Configure the Google Generative AI client
    # Ensure GOOGLE_API_KEY is set in your environment variables
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    # Initialize the Generative Model
    model = genai.GenerativeModel('gemini-pro')

    # Generate content (summary)
    response = model.generate_content(f"Summarize the following meeting transcript chunk:

{transcript_chunk}")

    return response.text.strip()

if __name__ == "__main__":
    # Example usage:
    example_chunk = """
    Facilitator: Welcome everyone to today's sync-up. Let's start with project Alpha. Sarah, any updates on the development front?
    Sarah: Yes, we've completed the backend integration, and it's currently in testing. We found a minor bug related to user authentication, which our team is actively working on. We expect a fix by end of day.
    John: That's great, Sarah. What about the frontend? Is it ready for the next sprint?
    Sarah: The frontend team has made significant progress, but we still need to integrate with the new API endpoints once the backend bug is resolved.
    Facilitator: Okay, so the blocker is the backend authentication bug. John, can you prioritize resources to help Sarah's team resolve this?
    John: Absolutely. I'll reallocate resources immediately. We should have a resolution soon.
    Facilitator: Excellent. Moving on to project Beta...
    """
    summary = summarize_transcript_chunk(example_chunk)
    print("Summary of the transcript chunk:")
    print(summary)
