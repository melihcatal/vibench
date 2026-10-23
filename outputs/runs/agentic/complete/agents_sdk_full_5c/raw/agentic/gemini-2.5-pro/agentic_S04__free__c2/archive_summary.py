from speech_client import cohere_client
from speech_models import SummaryResult

def summarize_transcript_cohere(transcript_text: str) -> SummaryResult:
    """
    Summarizes a long transcript text using the Cohere Summarize API.

    Args:
        transcript_text: The full transcript text to summarize.

    Returns:
        A SummaryResult object containing the summary.
    """
    response = cohere_client.summarize(
        text=transcript_text,
        model="command",  # Cohere's generative model
        length="medium",
        format="paragraph"
    )
    
    return SummaryResult(
        original_text=transcript_text,
        summary=response.summary
    )
