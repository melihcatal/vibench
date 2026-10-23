import os
import cohere

def output_embedding(texts: list[str]) -> list[list[float]]:
    api_key = os.getenv('COHERE_API_KEY')
    if not api_key:
        raise ValueError('COHERE_API_KEY environment variable is required.')
    co = cohere.Client(api_key)
    response = co.embed(
        texts=texts,
        model='embed-english-v3.0'
    )
    return response.embeddings
