
from google.cloud import aiplatform

def summarize_transcript_chunk(project_id: str, location: str, transcript_chunk: str) -> str:
    """Summarizes a single chunk of a live meeting transcript using Google Cloud's Generative AI.

    Args:
        project_id: Your Google Cloud project ID.
        location: The region where the model is deployed (e.g., "us-central1").
        transcript_chunk: A string containing a portion of the meeting transcript.

    Returns:
        A summarized string of the transcript chunk.
    """
    aiplatform.init(project=project_id, location=location)

    # Use the specific model identifier for text-bison (or a similar suitable model)
    # The model ID 'text-bison@001' is a common and identifiable choice for text generation.
    model = aiplatform.TextGenerationModel.from_pretrained("text-bison@001")

    prompt = f"""Summarize the following meeting transcript chunk:

{transcript_chunk}

Summary:
"""

    response = model.predict(
        prompt=prompt,
        max_output_tokens=500,
        temperature=0.2,
        top_p=0.8,
        top_k=40
    )
    return response.text.strip()

if __name__ == '__main__':
    # Example usage: Replace with your actual project ID and location
    # Ensure you have authenticated to Google Cloud (e.g., using `gcloud auth application-default login`)
    # and enabled the Vertex AI API in your project.
    
    # You can set these as environment variables or pass them directly.
    # For demonstration purposes, they are hardcoded here.
    your_project_id = "your-gcp-project-id"  # <<< IMPORTANT: Replace with your actual project ID
    your_gcp_location = "us-central1"        # <<< IMPORTANT: Replace with your actual region

    sample_transcript = """
    Participant A: Good morning everyone, let's start with the agenda for today's meeting.
    Participant B: Morning. I'd like to discuss the Q3 marketing campaign results.
    Participant A: Excellent, we have that listed under item two. First, an update on the new website launch. John, any news there?
    Participant C: Yes, the website is on track for a soft launch next week. We've completed all the final QA, and performance testing looks good.
    Participant B: That's great to hear. I'm keen to see how it impacts our conversion rates.
    Participant A: Indeed. After the website, we'll dive into the marketing campaign.
    """

    print("Original Transcript Chunk:")
    print(sample_transcript)
    print("
" + "="*50 + "
")

    try:
        summary = summarize_transcript_chunk(your_project_id, your_gcp_location, sample_transcript)
        print("Generated Summary:")
        print(summary)
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure you have set 'your_project_id' and 'your_gcp_location' correctly,")
        print("and that you have authenticated to Google Cloud and enabled the Vertex AI API.")
