import os
import cohere

def summarize_meeting_chunk(transcript_chunk: str):
    """
    Summarizes a chunk of a meeting transcript using the Cohere API.

    Args:
        transcript_chunk: A string containing a portion of the meeting transcript.

    Returns:
        The summary text, or None if an error occurs.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    try:
        co = cohere.Client(api_key)
        # Using a recommended model like 'command' for summarization tasks
        response = co.summarize(
            text=transcript_chunk,
            model='command',
            length='medium',
            format='paragraph'
        )
        return response.summary
    except cohere.CohereError as e:
        print(f"An error occurred with the Cohere API: {e}")
        return None
