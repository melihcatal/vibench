from model_client import get_cohere_client

def summarize_text(long_text: str) -> str:
    """
    Summarizes a long piece of text using the Cohere Summarize API.
    """
    client = get_cohere_client()
    
    # Using a model from the "summarize" family specifically for this task
    response = client.summarize(
        text=long_text,
        model='summarize-xlarge',
        length='medium',
        format='paragraph'
    )
    
    return response.summary
