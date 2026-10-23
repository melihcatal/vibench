import os
import cohere

def transcript_embedding(texts: list[str]) -> list[list[float]]:
    api_key = os.getenv('COHERE_API_KEY')
    if not api_key:
        raise ValueError('COHERE_API_KEY environment variable is required.')
    client = cohere.Client(api_key)
    response = client.embed(
        texts=texts,
        model='embed-english-v3.0'
    )
    return response.embeddings