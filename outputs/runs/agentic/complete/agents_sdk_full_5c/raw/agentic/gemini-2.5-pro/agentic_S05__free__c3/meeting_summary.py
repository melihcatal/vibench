import os
import cohere
from speech_models import SummaryResult

def summarize_meeting_transcript(transcript: str) -> SummaryResult:
    """
    Summarizes a chunk of a live meeting transcript using Cohere.

    Requires COHERE_API_KEY environment variable to be set.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    response = co.summarize(
        text=transcript,
        model='command',
        length='medium',
        extractiveness='low'
    )

    return SummaryResult(
        original_text=transcript,
        summary=response.summary
    )
