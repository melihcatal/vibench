import os
import cohere


def summarize_transcript(transcript_text: str) -> str:
    """
    Summarize transcription results using Cohere.
    """
    cohere_api_key = os.getenv("COHERE_API_KEY")
    if not cohere_api_key:
        raise ValueError("COHERE_API_KEY must be set.")

    co = cohere.Client(cohere_api_key)

    response = co.summarize(
        text=transcript_text, model="command", length="medium", extractiveness="low"
    )

    return response.summary
