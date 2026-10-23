import os
import cohere


def archive_summary(transcript_text: str) -> str:
    """
    Summarizes transcription results using Cohere.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set")

    co = cohere.Client(api_key)

    response = co.summarize(
        text=transcript_text, model="command", length="medium", extractiveness="low"
    )

    return response.summary
