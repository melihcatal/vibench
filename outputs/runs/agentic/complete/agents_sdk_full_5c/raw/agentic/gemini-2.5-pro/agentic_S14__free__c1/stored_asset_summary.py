import os
import cohere
from storage_models import SummaryResult

def summarize_text_cohere(text_to_summarize: str) -> SummaryResult:
    """
    Summarizes text using the Cohere Summarize API.

    Requires the COHERE_API_KEY environment variable to be set.

    Args:
        text_to_summarize (str): The text content to summarize.

    Returns:
        A SummaryResult object containing the summary.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    # Use a specific Cohere model for summarization
    model = 'summarize-xlarge'
    
    response = co.summarize(
        text=text_to_summarize,
        model=model,
        length='medium',
        extractiveness='low'
    )

    return SummaryResult(
        id=response.id,
        summary=response.summary,
        source_text=text_to_summarize,
        model=model
    )
