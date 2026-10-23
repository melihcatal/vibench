import os
import cohere
from model_client import COHERE_API_KEY

def summarize_text(text_to_summarize: str) -> str:
    """
    Summarizes a long text using the Cohere API.
    """
    if not COHERE_API_KEY:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(COHERE_API_KEY)
    
    response = co.summarize(
        text=text_to_summarize,
        model='command-r',
        length='medium',
        extractiveness='medium'
    )
    
    return response.summary
