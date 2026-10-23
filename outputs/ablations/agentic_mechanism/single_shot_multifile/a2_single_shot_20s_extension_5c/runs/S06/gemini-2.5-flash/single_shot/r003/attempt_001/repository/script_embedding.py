import os
import cohere

def embed_script_cohere(texts: list[str], model: str = 'embed-english-v3.0') -> list[list[float]]:
    api_key = os.environ.get('COHERE_API_KEY')
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")
    co = cohere.Client(api_key=api_key)
    response = co.embed(texts=texts, model=model)
    return response.embeddings
