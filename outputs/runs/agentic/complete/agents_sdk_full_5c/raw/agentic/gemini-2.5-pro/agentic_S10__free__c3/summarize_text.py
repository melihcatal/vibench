from model_client import get_cohere_client

def summarize_text(long_text: str) -> str:
    """
    Summarizes a long text using the Cohere API.

    Args:
        long_text: The text to be summarized.

    Returns:
        The summarized text.
    """
    cohere_client = get_cohere_client()
    
    # Provider-specific model ID: command-r
    response = cohere_client.summarize(
        text=long_text,
        model='command-r',
        length='medium',
        format='paragraph'
    )
    
    return response.summary
