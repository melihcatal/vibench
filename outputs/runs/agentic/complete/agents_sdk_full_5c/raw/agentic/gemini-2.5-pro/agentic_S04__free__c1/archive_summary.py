import os
import cohere

def summarize_transcript(transcript_text: str) -> str:
    """
    Summarizes a long transcript using the Cohere Summarize API.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")
    
    co = cohere.Client(api_key)

    response = co.summarize(
        text=transcript_text,
        model='command-r',
        length='medium',
        format='paragraph'
    )

    return response.summary
