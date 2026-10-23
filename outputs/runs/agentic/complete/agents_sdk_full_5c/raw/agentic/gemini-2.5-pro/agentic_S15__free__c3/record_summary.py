import os
import cohere
from typing import Dict, Any

def record_summary(record: Dict[str, Any], text_field: str) -> str:
    """
    Summarizes a text field from a retrieved document record using Cohere.

    Args:
        record: The document record.
        text_field: The key of the text field to summarize.

    Returns:
        The summarized text.
    """
    cohere_api_key = os.getenv("COHERE_API_KEY")
    if not cohere_api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(cohere_api_key)

    text_to_summarize = record.get(text_field)
    if not text_to_summarize:
        return ""

    response = co.summarize(
        text=text_to_summarize,
        model='command-r',
        length='medium',
        format='paragraph'
    )

    return response.summary
