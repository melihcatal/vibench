import os
import cohere
from speech_models import TranscriptionResponse


def summarize_transcript(transcript: TranscriptionResponse) -> str:
    """
    Summarizes a transcription using Cohere's Summarize API.
    """
    cohere_api_key = os.environ.get("COHERE_API_KEY")
    co = cohere.Client(cohere_api_key)

    if not transcript.text:
        return ""

    response = co.summarize(
        text=transcript.text,
        model="summarize-xlarge",
        length="medium",
        format="paragraph",
    )

    return response.summary
