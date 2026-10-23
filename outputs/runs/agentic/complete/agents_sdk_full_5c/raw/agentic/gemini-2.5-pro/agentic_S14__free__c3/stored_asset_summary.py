import os
import cohere
from . import storage_models

def summarize_text_content(text: str) -> storage_models.SummaryResult:
    """
    Summarizes extracted text content using the Cohere API.

    Args:
        text: The text content to summarize.

    Returns:
        A SummaryResult object.
    """
    cohere_api_key = os.environ.get("COHERE_API_KEY")
    if not cohere_api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(cohere_api_key)
    
    # Using the 'command-r' model for summarization
    model_id = 'command-r'

    response = co.summarize(
        text=text,
        model=model_id,
        length='medium',
        format='paragraph'
    )

    summary = response.summary

    return storage_models.SummaryResult(
        source_text_length=len(text),
        summary_text=summary,
        model_id=model_id
    )
