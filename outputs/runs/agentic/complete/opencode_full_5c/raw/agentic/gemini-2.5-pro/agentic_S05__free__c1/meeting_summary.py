import os
import cohere
from speech_models import SummaryResponse


def summarize_meeting_transcript(
    transcript_chunks: list[str],
) -> SummaryResponse | None:
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    full_transcript = " ".join(transcript_chunks)

    if not full_transcript.strip():
        return None

    try:
        response = co.summarize(
            text=full_transcript,
            model="command-r",
            length="medium",
            extractiveness="low",
        )
        return SummaryResponse(summary=response.summary)
    except cohere.CohereError as e:
        print(f"Cohere API error: {e}")
        return None
