import os
import cohere

def summarize_meeting_chunk(transcript_chunk: str) -> str:
    """
    Summarizes a chunk of a meeting transcript using the Cohere API.

    Args:
        transcript_chunk: A string containing a portion of the meeting transcript.

    Returns:
        The summarized text.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise EnvironmentError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    try:
        response = co.summarize(
            text=transcript_chunk,
            model="summarize-xlarge",  # Cohere's summarization-specific model
            length="medium",
            format="paragraph",
            extractiveness="low",
        )
        return response.summary
    except cohere.CohereError as e:
        return f"Cohere API error: {e}"

