import os
from google.cloud import aiplatform

def summarize_meeting_chunks(transcript_chunks: list[str]) -> str:
    """
    Summarizes live meeting transcript chunks using Google Cloud Vertex AI.

    Args:
        transcript_chunks: A list of transcript chunks (strings).

    Returns:
        A string containing the summary of the transcript chunks.
    """
    aiplatform.init(project=os.environ.get("GOOGLE_CLOUD_PROJECT"))

    model = aiplatform.TextGenerationModel.from_pretrained("text-bison")
    
    # Combine chunks into a single text for summarization
    full_transcript = " ".join(transcript_chunks)

    prompt = f"""Summarize the following meeting transcript:
{full_transcript}
"""

    response = model.predict(
        prompt,
        temperature=0.2,
        max_output_tokens=256,
        top_p=0.8,
        top_k=40,
    )

    return response.text
